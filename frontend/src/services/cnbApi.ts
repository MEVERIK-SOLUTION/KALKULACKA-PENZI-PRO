/**
 * ČNB (Czech National Bank) API Service
 * Dokumentace: 4.7 - ČNB ARAD (statistika)
 * URL: https://www.cnb.cz/aradb/api/v1
 */

export interface CNBExchangeRate {
  currency: string;
  code: string;
  rate: number;
  date: string;
}

export interface CNBInflation {
  indicatorId: string;
  date: string;
  value: number;
  description: string;
}

/**
 * Get exchange rate from ČNB
 * Indicator: SMV5M603 (směnný kurz)
 * Example: curl "https://www.cnb.cz/aradb/api/v1/data?indicator_id_list=SMV5M603&api_key=YOUR_KEY"
 */
export async function getExchangeRate(
  currency: string = 'EUR',
  apiKey?: string
): Promise<number> {
  try {
    const indicatorMap: Record<string, string> = {
      'EUR': 'SMV5M603', // EUR
      'USD': 'SMV5M604', // USD
      'GBP': 'SMV5M605', // GBP
    };

    const indicator = indicatorMap[currency] || 'SMV5M603';
    let url = `https://www.cnb.cz/aradb/api/v1/data?indicator_id_list=${indicator}`;
    
    if (apiKey) {
      url += `&api_key=${apiKey}`;
    }

    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`ČNB API error: ${response.statusText}`);
    }

    const data = await response.json();
    
    // Parse exchange rate from response
    // Format: { "data": [{ "datum": "2026-05-07", "hodnota": "24.50", ... }] }
    if (data?.data && data.data.length > 0) {
      return parseFloat(data.data[0].hodnota) || 0;
    }

    return 0;
  } catch (error) {
    console.error('Chyba při získávání kurzu z ČNB:', error);
    return 0; // Fallback
  }
}

/**
 * Get inflation rate from ČNB
 * Indicator: CPI (consumer price index)
 * Example: SMV5M603 for inflation
 */
export async function getCNBInflation(
  indicatorId: string = 'SMV5M603',
  monthsBefore: number = 12,
  apiKey?: string
): Promise<number> {
  try {
    let url = `https://www.cnb.cz/aradb/api/v1/data?indicator_id_list=${indicatorId}&months_before=${monthsBefore}`;
    
    if (apiKey) {
      url += `&api_key=${apiKey}`;
    }

    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`ČNB API error: ${response.statusText}`);
    }

    const data = await response.json();
    
    if (data?.data && data.data.length > 0) {
      // Get the latest value
      const latest = data.data[data.data.length - 1];
      return parseFloat(latest.hodnota) || 0;
    }

    return 0;
  } catch (error) {
    console.error('Chyba při získávání inflace z ČNB:', error);
    return 0; // Fallback to 2.5%
  }
}

/**
 * Get multiple economic indicators
 * Used for pension adjustment calculations
 */
export async function getEconomicIndicators(apiKey?: string): Promise<{
  inflationRate: number;
  eurRate: number;
  usdRate: number;
}> {
  try {
    const [inflation, eurRate, usdRate] = await Promise.all([
      getCNBInflation('SMV5M603', 12, apiKey),
      getExchangeRate('EUR', apiKey),
      getExchangeRate('USD', apiKey),
    ]);

    return {
      inflationRate: inflation || 2.5, // Default 2.5%
      eurRate: eurRate || 24.50,
      usdRate: usdRate || 22.50,
    };
  } catch (error) {
    console.error('Chyba při získávání ekonomických ukazatelů:', error);
    return {
      inflationRate: 2.5,
      eurRate: 24.50,
      usdRate: 22.50,
    };
  }
}

/**
 * Search legislation in e-Sbírka (free access)
 * Dokumentace: 4.8 - e-Sbírka
 * URL: https://www.e-sbirka.cz
 */
export async function searchLegislation(query: string): Promise<any[]> {
  try {
    // e-Sbírka doesn't have a public search API without registration
    // This is a simplified version - in production, use proper API
    const url = `https://www.e-sbirka.cz/api/search?q=${encodeURIComponent(query)}`;
    
    const response = await fetch(url);
    
    if (!response.ok) {
      // Fallback to mock data
      return [
        { id: '155/1995', title: 'Zákon o důchodovém pojištění', type: 'zákon' },
        { id: '290/2025', title: 'Vyhláška o důchodovém pojištění', type: 'vyhláška' },
      ];
    }

    return await response.json();
  } catch (error) {
    console.error('Chyba při vyhledávání v e-Sbírce:', error);
    return [];
  }
}

/**
 * Get data from Portál ČSSZ (requires login)
 * Dokumentace: 9 - ČSSZ ePortál
 * Note: This requires BankID/NIA authentication
 */
export function getCSSZInfo(): { url: string; note: string } {
  return {
    url: 'https://eportal.cssz.cz',
    note: 'Vyžaduje přihlášení přes BankID/NIA. Pro vývojáře: požádat o vzorový IOLDP soubor.',
  };
}
