/**
 * ČSÚ (Czech Statistical Office) API Service
 * Dokumentace: 4.7 - ČSÚ Statisticke API
 * URL: https://data.csu.gov.cz
 */

export interface InflationData {
  year: number;
  month: number;
  rate: number; // Procentní inflace
  source: string;
}

export interface CSUSearchResult {
  id: string;
  title: string;
  url: string;
}

/**
 * Get inflation rate for a specific year
 * Indikátor: CRUHVD1T2 (průměrná inflace za rok)
 * Example: curl "https://data.csu.gov.cz/api/dotaz/v1/data/sady/CRUHVD1T2?format=json"
 */
export async function getInflationRate(year: number): Promise<number> {
  try {
    const url = `https://data.csu.gov.cz/api/dotaz/v1/data/sady/CRUHVD1T2?format=json&rok=${year}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`ČSÚ API error: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    // Parse inflation from response
    // Format: { "data": [{"rok": "2026", "hodnota": "2.5"}, ...] }
    if (data?.data && data.data.length > 0) {
      const item = data.data.find((d: any) => d.rok == year);
      return item ? parseFloat(item.hodnota) : 0;
    }
    
    return 0;
  } catch (error) {
    console.error('Chyba při získávání inflace z ČSÚ:', error);
    return 0; // Fallback
  }
}

/**
 * Get average wage for a specific year
 * Used for base pension calculation (§ 4 odst. 2 ZDP)
 */
export async function getAverageWage(year: number): Promise<number> {
  try {
    // Toto je zjednodušené - v produkci by se mělo volat skutečné ČSÚ API
    // Pro ukázku vracíme odhad
    const baseWage2026 = 49262;
    const estimatedIncrease = 0.05; // 5% růst
    
    if (year === 2026) return baseWage2026;
    return baseWage2026 * Math.pow(1 + estimatedIncrease, year - 2026);
  } catch (error) {
    console.error('Chyba při získávání průměrné mzdy:', error);
    return 49262; // Fallback na 2026
  }
}

/**
 * Search datasets in ČSÚ Open Data
 */
export async function searchCSUSDatasets(query: string): Promise<CSUSearchResult[]> {
  try {
    const url = `https://data.csu.gov.cz/api/dotaz/v1/datove-sady?dotaz=${encodeURIComponent(query)}&format=json`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`ČSÚ API error: ${response.statusText}`);
    }
    
    const data = await response.json();
    return data?.data || [];
  } catch (error) {
    console.error('Chyba při vyhledávání v ČSÚ:', error);
    return [];
  }
}

/**
 * Get dataset by ID
 * Example: MZDO1 (mzdy)
 */
export async function getCSUSDataset(datasetId: string): Promise<any> {
  try {
    const url = `https://data.csu.gov.cz/api/dotaz/v1/data/sady/${datasetId}?format=json`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`ČSÚ API error: ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`Chyba při získávání datasetu ${datasetId}:`, error);
    return null;
  }
}
