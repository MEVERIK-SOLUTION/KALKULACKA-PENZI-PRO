/**
 * IOLDP Parser Service
 * Parses XML data from ČSSZ ePortál
 * Dokumentace: 5.1 - IOLDP XML/PDF
 */

export interface IOLDPData {
  fullName: string;
  birthDate: string;
  insuranceYears: number;
  annualIncomes: Array<{
    year: number;
    income: number;
    coefficient: number;
  }>;
  excludedDays: number;
  substituteDays: number;
}

export interface ParseResult {
  success: boolean;
  data?: IOLDPData;
  error?: string;
}

/**
 * Parse XML string from IOLDP
 * Expected XML structure based on ČSSZ ePortál documentation
 */
export function parseIOLDPXML(xmlText: string): ParseResult {
  try {
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlText, 'text/xml');

    // Check for parsing errors
    const parserError = xmlDoc.querySelector('parsererror');
    if (parserError) {
      return {
        success: false,
        error: 'Neplatný XML formát',
      };
    }

    // Extract personal data
    const fullName = getXMLValue(xmlDoc, 'jmeno') || getXMLValue(xmlDoc, 'name') || '';
    const birthDate = getXMLValue(xmlDoc, 'datumNarozeni') || getXMLValue(xmlDoc, 'birthDate') || '';

    // Extract insurance years
    const insuranceYearsStr = getXMLValue(xmlDoc, 'dobaPojisteni') || getXMLValue(xmlDoc, 'insuranceYears') || '0';
    const insuranceYears = parseFloat(insuranceYearsStr) || 0;

    // Extract annual incomes
    const annualIncomes: Array<{ year: number; income: number; coefficient: number }> = [];
    const incomeElements = xmlDoc.querySelectorAll('prijem, income, rocniPrijem');
    
    incomeElements.forEach((el, index) => {
      const year = parseInt(el.getAttribute('rok') || el.getAttribute('year') || `${2026 - index}`);
      const income = parseFloat(el.textContent || '0');
      const coefficient = parseFloat(el.getAttribute('koeficient') || el.getAttribute('coefficient') || '1.0581');
      
      if (income > 0) {
        annualIncomes.push({ year, income, coefficient });
      }
    });


    // Extract excluded days
    const excludedDaysStr = getXMLValue(xmlDoc, 'vylouceneDny') || getXMLValue(xmlDoc, 'excludedDays') || '0';
    const excludedDays = parseInt(excludedDaysStr) || 0;

    // Extract substitute days
    const substituteDaysStr = getXMLValue(xmlDoc, 'nahradniDoby') || getXMLValue(xmlDoc, 'substituteDays') || '0';
    const substituteDays = parseInt(substituteDaysStr) || 0;

    const data: IOLDPData = {
      fullName,
      birthDate,
      insuranceYears,
      annualIncomes,
      excludedDays,
      substituteDays,
    };

    return { success: true, data };
  } catch (error) {
    return {
      success: false,
      error: `Chyba při parsování XML: ${error instanceof Error ? error.message : 'Neznámá chyba'}`,
    };
  }
}

/**
 * Parse PDF text from IOLDP
 * Note: PDF parsing requires server-side processing or PDF.js library
 * This is a simplified text-based parser
 */
export function parseIOLDPPDF(pdfText: string): ParseResult {
  try {
    // Extract data using regex patterns
    const nameMatch = pdfText.match(/jméno[:\s]*([^\n]+)/i);
    const birthMatch = pdfText.match(/datum narození[:\s]*([^\n]+)/i);
    
    const data: IOLDPData = {
      fullName: nameMatch ? nameMatch[1].trim() : '',
      birthDate: birthMatch ? birthMatch[1].trim() : '',
      insuranceYears: 0,
      annualIncomes: [],
      excludedDays: 0,
      substituteDays: 0,
    };

    // Extract years of insurance
    const yearsMatch = pdfText.match(/doba pojištění[:\s]*(\d+)\s*let/i);
    if (yearsMatch) {
      data.insuranceYears = parseInt(yearsMatch[1]) || 0;
    }

    // Extract annual incomes (simplified)
    const incomePattern = /(\d{4})[:\s]*([\d\s]+)\s*Kč/gi;
    let match;
    while ((match = incomePattern.exec(pdfText)) !== null) {
      const year = parseInt(match[1]);
      const income = parseFloat(match[2].replace(/\s/g, '')) || 0;
      if (year > 2000 && income > 0) {
        data.annualIncomes.push({
          year,
          income,
          coefficient: 1.0581, // Default for 2026
        });
      }
    }

    return { success: true, data };
  } catch (error) {
    return {
      success: false,
      error: `Chyba při parsování PDF: ${error instanceof Error ? error.message : 'Neznámá chyba'}`,
    };
  }
}

/**
 * Helper: Get value from XML element
 */
function getXMLValue(doc: Document, tagName: string): string {
  const element = doc.querySelector(tagName);
  return element ? element.textContent || '' : '';
}

/**
 * Convert IOLDP data to calculator format
 */
export function mapToCalculatorInput(iolDPData: IOLDPData) {
  return {
    annual_incomes: iolDPData.annualIncomes.map(item => item.income),
    coefficients: iolDPData.annualIncomes.map(item => item.coefficient),
    insurance_years: iolDPData.insuranceYears,
    excluded_days: iolDPData.excludedDays,
    substitute_days: iolDPData.substituteDays,
  };
}
