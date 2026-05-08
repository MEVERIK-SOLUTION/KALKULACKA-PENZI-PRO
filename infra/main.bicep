@description('Azure region for deployment')
param location string = resourceGroup().location

@description('Name of the Container Apps environment')
param environmentName string = 'pension-api-env'

@description('Name of the Container App')
param containerAppName string = 'pension-api'

@description('Container image (format: <registry>/<repo>:<tag>)')
param containerImage string = 'pension-api:latest'

@description('API Keys for authentication')
@secure()
param apiKeys string

@description('Redis connection string')
@secure()
param redisUrl string = 'redis://redis:6379/0'

@description('PostgreSQL connection string')
@secure()
param databaseUrl string

@description('CORS origins')
param corsOrigins string = '["https://kalkulacka-penzi-pro.pages.dev"]'

@description('Log Analytics workspace name')
param logAnalyticsWorkspaceName string = 'pension-api-logs'

var containerAppsContributorRoleId = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '/providers/Microsoft.Authorization/roleDefinitions/ed7f3fbd-7b88-4dd4-9017-9adb7ce333f8')

resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsWorkspaceName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: environmentName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspace.properties.customerId
        sharedKey: logAnalyticsWorkspace.listKeys().primarySharedKey
      }
    }
  }
}

resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: containerAppName
  location: location
  properties: {
    managedEnvironmentId: containerAppsEnvironment.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
        traffic: [
          {
            latestRevision: true
            weight: 100
          }
        ]
      }
      secrets: [
        {
          name: 'api-keys'
          value: apiKeys
        }
        {
          name: 'database-url'
          value: databaseUrl
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'pension-api'
          image: containerImage
          env: [
            {
              name: 'FASTAPI_HOST'
              value: '0.0.0.0'
            }
            {
              name: 'FASTAPI_PORT'
              value: '8000'
            }
            {
              name: 'PORT'
              value: '8000'
            }
            {
              name: 'REDIS_URL'
              value: redisUrl
            }
            {
              name: 'DATABASE_URL'
              secretRef: 'database-url'
            }
            {
              name: 'API_KEYS'
              secretRef: 'api-keys'
            }
            {
              name: 'CORS_ORIGINS'
              value: corsOrigins
            }
            {
              name: 'DEBUG'
              value: 'False'
            }
            {
              name: 'PYTHONUNBUFFERED'
              value: '1'
            }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 10
        rules: [
          {
            name: 'http-rule'
            http: {
              metadata: {
                concurrentRequests: '100'
              }
            }
          }
        ]
      }
    }
  }
}
