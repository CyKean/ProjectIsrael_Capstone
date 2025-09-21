// weather.js - Multi-Provider Weather API with Fallback

// Configuration
const API_CONFIG = {
  primary: {
    name: 'Open-Meteo',
    baseUrl: 'https://api.open-meteo.com/v1',
    aqBaseUrl: 'https://air-quality-api.open-meteo.com/v1',
    endpoints: {
      forecast: '/forecast',
      airQuality: '/air-quality'
    }
  },
  fallback: {
    name: 'WeatherAPI',
    baseUrl: 'https://api.weatherapi.com/v1',
    endpoints: {
      forecast: '/forecast.json',
      current: '/current.json'
    },
    apiKey: 'be2785e8e2f44f11b2605501251508'
  }
};

const DEFAULT_LOCATION = {
  latitude: 13.405165290699628,
  longitude: 121.2151274080352
};

// Default data structures
const DEFAULT_RESPONSE = {
  current: {
    temperature_c: 0,
    weather_condition: 'Unknown',
    humidity: 0,
    wind_speed: 0,
    wind_direction: 0,
    precipitation: 0,
    rainChance: 0,
    uv_index: 0,
    pressure: 0,
    sunrise: '06:00',
    sunset: '18:00',
  },
  forecast: Array(10).fill({
    date: new Date().toISOString().split('T')[0],
    temperature_max: 0,
    temperature_min: 0,
    condition_code: 0,
  }),
  hourlyForecast: Array(10).fill({
    time: '00:00',
    temp: 0,
    condition: 'Unknown',
    rainChance: 0,
  }),
  airQuality: {
    pm2_5: 0,
    pm10: 0,
    carbon_monoxide: 0,
    nitrogen_dioxide: 0,
    ozone: 0,
    sulphur_dioxide: 0,
  },
  sunData: {
    sunrise: '06:00',
    sunset: '18:00',
  }
};

const DEFAULT_CITY_RESPONSE = {
  name: 'Unknown',
  condition: 'Unknown',
  temperature: 0,
  time: '00:00'
};

// Helper functions
const getRecentNonZero = (array, startIndex) => {
  if (!array) return 0;
  for (let i = startIndex; i >= 0; i--) {
    if (array[i] !== undefined && array[i] !== 0) return array[i];
  }
  for (let i = startIndex; i < array.length; i++) {
    if (array[i] !== undefined && array[i] !== 0) return array[i];
  }
  return 0;
};

// Return an ISO-like hour string for Asia/Manila matching Open-Meteo's hourly.time format
function getManilaIsoHourFromDate(date = new Date()) {
  // sv-SE produces 'YYYY-MM-DD HH:mm:ss' which is stable and sortable
  const manila = date.toLocaleString('sv-SE', { timeZone: 'Asia/Manila', hour12: false });
  // Convert to 'YYYY-MM-DDTHH:00'
  return manila.replace(' ', 'T').slice(0, 13) + ':00';
}

// Return year-month-day and hour number for Asia/Manila for comparisons
function getManilaYMDHourFromDate(date = new Date()) {
  const manila = date.toLocaleString('sv-SE', { timeZone: 'Asia/Manila', hour12: false });
  const ymd = manila.slice(0, 10); // 'YYYY-MM-DD'
  const hour = parseInt(manila.slice(11, 13), 10);
  return { ymd, hour };
}

// Data Processing Functions
function processOpenMeteoData(weatherData, aqData) {
  // Compute Manila-local current hour so we align with the API timezone=Asia/Manila
  const currentHour = getManilaIsoHourFromDate();
  let idx = weatherData.hourly?.time?.findIndex(t => t === currentHour) ?? -1;
  if (idx === -1) idx = 0; // fallback if exact match not found
  const todayIndex = 0;

  // Get the next 10 hours of data (current hour + next 9 hours)
  const hoursToShow = 10;

  return {
    current: {
      temperature_c: weatherData.current_weather?.temperature ?? 
                   getRecentNonZero(weatherData.hourly?.temperature_2m, idx),
      weather_condition: mapWeatherCode(weatherData.current_weather?.weathercode),
      humidity: getRecentNonZero(weatherData.hourly?.relative_humidity_2m, idx),
      wind_speed: getRecentNonZero(weatherData.hourly?.wind_speed_10m, idx),
      wind_direction: getRecentNonZero(weatherData.hourly?.wind_direction_10m, idx),
      precipitation: getRecentNonZero(weatherData.hourly?.precipitation, idx),
      rainChance: getRecentNonZero(weatherData.hourly?.precipitation_probability, idx),
      uv_index: getRecentNonZero(weatherData.hourly?.uv_index, idx),
      pressure: getRecentNonZero(weatherData.hourly?.surface_pressure, idx),
      sunrise: weatherData.daily?.sunrise?.[todayIndex] ?? '06:00',
      sunset: weatherData.daily?.sunset?.[todayIndex] ?? '18:00',
    },
    forecast: weatherData.daily?.time?.map((date, i) => ({
      date,
      temperature_max: weatherData.daily.temperature_2m_max?.[i] ?? 0,
      temperature_min: weatherData.daily.temperature_2m_min?.[i] ?? 0,
      condition_code: weatherData.daily.weathercode?.[i] ?? 0,
    })) || DEFAULT_RESPONSE.forecast,
    hourlyForecast: weatherData.hourly?.time?.slice(idx, idx + hoursToShow).map((t, i) => ({
      time: new Date(t).toLocaleTimeString('en-PH', { hour: '2-digit', minute: '2-digit', hour12: true }),
      temp: weatherData.hourly.temperature_2m?.[idx + i] ?? 0,
      condition: mapWeatherCode(weatherData.hourly.weathercode?.[idx + i]),
      rainChance: weatherData.hourly.precipitation_probability?.[idx + i] ?? 0,
    })) || DEFAULT_RESPONSE.hourlyForecast,
    airQuality: {
      pm2_5: aqData.hourly?.pm2_5?.[0] ?? 0,
      pm10: aqData.hourly?.pm10?.[0] ?? 0,
      carbon_monoxide: aqData.hourly?.carbon_monoxide?.[0] ?? 0,
      nitrogen_dioxide: aqData.hourly?.nitrogen_dioxide?.[0] ?? 0,
      ozone: aqData.hourly?.ozone?.[0] ?? 0,
      sulphur_dioxide: aqData.hourly?.sulphur_dioxide?.[0] ?? 0,
    },
    sunData: {
      sunrise: formatTimeToPH(weatherData.daily?.sunrise?.[todayIndex]) ?? '06:00 AM',
      sunset: formatTimeToPH(weatherData.daily?.sunset?.[todayIndex]) ?? '06:00 PM',
    }
  };
}

function processWeatherApiData(data) {
  const current = data.current;
  const hourlyData = data.forecast?.forecastday?.[0]?.hour || [];
  // Determine current Manila date/hour and find the matching hourly entry
  const manilaNow = getManilaYMDHourFromDate(new Date());
  let currentHourIndex = hourlyData.findIndex(hour => {
    try {
      const d = new Date(hour.time);
      const parts = getManilaYMDHourFromDate(d);
      return parts.ymd === manilaNow.ymd && parts.hour === manilaNow.hour;
    } catch (e) {
      return false;
    }
  });
  if (currentHourIndex === -1) {
    // fallback: try matching by hour number only
    currentHourIndex = hourlyData.findIndex(hour => new Date(hour.time).getHours() === manilaNow.hour);
  }
  if (currentHourIndex === -1) currentHourIndex = 0;

  const hoursToShow = 10;

  return {
    current: {
      temperature_c: current?.temp_c ?? 0,
      weather_condition: current?.condition?.text || 'Unknown',
      humidity: current?.humidity ?? 0,
      wind_speed: current?.wind_kph ?? 0,
      wind_direction: current?.wind_degree ?? 0,
      precipitation: current?.precip_mm ?? 0,
      rainChance: hourlyData[currentHourIndex]?.chance_of_rain ?? 0,
      uv_index: current?.uv ?? 0,
      pressure: current?.pressure_mb ?? 0,
      sunrise: data.forecast?.forecastday?.[0]?.astro?.sunrise || '06:00 AM',
      sunset: data.forecast?.forecastday?.[0]?.astro?.sunset || '06:00 PM',
    },
    forecast: data.forecast?.forecastday?.map(day => ({
      date: day.date,
      temperature_max: day.day?.maxtemp_c ?? 0,
      temperature_min: day.day?.mintemp_c ?? 0,
      condition_code: mapWeatherCodeFromText(day.day?.condition?.text),
    })) || DEFAULT_RESPONSE.forecast,
    hourlyForecast: hourlyData.slice(currentHourIndex, currentHourIndex + hoursToShow).map(hour => ({
      time: new Date(hour.time).toLocaleTimeString('en-PH', { hour: '2-digit', minute: '2-digit', hour12: true }),
      temp: hour.temp_c ?? 0,
      condition: hour.condition?.text || 'Unknown',
      rainChance: hour.chance_of_rain ?? 0,
    })) || DEFAULT_RESPONSE.hourlyForecast,
    airQuality: DEFAULT_RESPONSE.airQuality,
    sunData: {
      sunrise: data.forecast?.forecastday?.[0]?.astro?.sunrise || '06:00 AM',
      sunset: data.forecast?.forecastday?.[0]?.astro?.sunset || '06:00 PM',
    }
  };
}

// Helper function to format time to Philippine format
function formatTimeToPH(isoTime) {
  if (!isoTime) return '';
  const date = new Date(isoTime);
  return date.toLocaleTimeString('en-PH', { hour: '2-digit', minute: '2-digit', hour12: true });
}

// Main Weather Data Function
export async function getWeatherData() {
  try {
    // Try primary API (Open-Meteo) first
    try {
      const [weatherData, aqData] = await Promise.all([
        fetch(`${API_CONFIG.primary.baseUrl}${API_CONFIG.primary.endpoints.forecast}?latitude=${DEFAULT_LOCATION.latitude}&longitude=${DEFAULT_LOCATION.longitude}&current_weather=true&hourly=temperature_2m,weathercode,relative_humidity_2m,wind_speed_10m,wind_direction_10m,precipitation,precipitation_probability,uv_index,surface_pressure&daily=temperature_2m_max,temperature_2m_min,weathercode,sunrise,sunset&timezone=Asia/Manila&forecast_days=10`)
          .then(r => r.ok ? r.json() : Promise.reject(new Error(`Status ${r.status}`))),
        
        fetch(`${API_CONFIG.primary.aqBaseUrl}${API_CONFIG.primary.endpoints.airQuality}?latitude=${DEFAULT_LOCATION.latitude}&longitude=${DEFAULT_LOCATION.longitude}&hourly=pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide&timezone=Asia/Manila`)
          .then(r => r.ok ? r.json() : Promise.reject(new Error(`Status ${r.status}`)))
      ]);
      
      return processOpenMeteoData(weatherData, aqData);
    } catch (primaryError) {
      console.warn('Primary API failed, trying fallback:', primaryError.message);
      
      // Fallback to WeatherAPI.com
      const weatherApiUrl = `${API_CONFIG.fallback.baseUrl}${API_CONFIG.fallback.endpoints.forecast}?key=${API_CONFIG.fallback.apiKey}&q=${DEFAULT_LOCATION.latitude},${DEFAULT_LOCATION.longitude}&days=10&aqi=no`;
      const weatherApiData = await fetch(weatherApiUrl)
        .then(r => r.ok ? r.json() : Promise.reject(new Error(`Fallback API failed with status ${r.status}`)));
      
      return processWeatherApiData(weatherApiData);
    }
  } catch (error) {
    console.error('All weather API attempts failed:', error);
    return DEFAULT_RESPONSE;
  }
}

// Weather Code Mapping
export function mapWeatherCode(code) {
  const mapping = {
    0: 'Clear',
    1: 'Mainly Clear',
    2: 'Partly Cloudy',
    3: 'Overcast',
    45: 'Fog',
    48: 'Depositing Rime Fog',
    51: 'Light Drizzle',
    53: 'Moderate Drizzle',
    55: 'Dense Drizzle',
    61: 'Light Rain',
    63: 'Moderate Rain',
    65: 'Heavy Rain',
    66: 'Freezing Rain',
    67: 'Heavy Freezing Rain',
    71: 'Light Snowfall',
    73: 'Moderate Snowfall',
    75: 'Heavy Snowfall',
    80: 'Rain Showers',
    81: 'Heavy Rain Showers',
    82: 'Violent Rain Showers',
    95: 'Thunderstorm',
    96: 'Thunderstorm with Hail',
    99: 'Severe Thunderstorm',
  };
  return mapping[code] || 'Unknown';
}

function mapWeatherCodeFromText(text) {
  const textToCode = {
    'Sunny': 0,
    'Clear': 0,
    'Partly cloudy': 2,
    'Cloudy': 3,
    'Overcast': 3,
    'Mist': 45,
    'Fog': 45,
    'Light rain': 61,
    'Moderate rain': 63,
    'Heavy rain': 65,
    'Light snow': 71,
    'Moderate snow': 73,
    'Heavy snow': 75,
    'Thunderstorm': 95,
  };
  return textToCode[text] || 0;
}

// Popular Cities Function with Fallback
export async function getWeatherDataForPopularCities() {
  const barangays = [
    { name: 'Bulusan', latitude: 13.4037, longitude: 121.2012 },
    { name: 'Suqui', latitude: 13.4177, longitude: 121.2040 },
    { name: 'Santo Niño', latitude: 13.4066, longitude: 121.1848 },
    { name: 'Ilaya (Poblacion)', latitude: 13.4129, longitude: 121.1840 },
    { name: 'Silonay', latitude: 13.3992, longitude: 121.2248 }
  ];
  
  try {
    const results = await Promise.all(
      barangays.map(async (barangay) => {
        try {
          // Try primary API first
          const primaryUrl = `${API_CONFIG.primary.baseUrl}${API_CONFIG.primary.endpoints.forecast}?latitude=${barangay.latitude}&longitude=${barangay.longitude}&current_weather=true&timezone=Asia/Manila`;
          const primaryResponse = await fetch(primaryUrl);
          
          if (primaryResponse.ok) {
            const data = await primaryResponse.json();
            return formatCityData(barangay.name, data);
          }
          
          // Fallback to WeatherAPI
          const fallbackUrl = `${API_CONFIG.fallback.baseUrl}${API_CONFIG.fallback.endpoints.current}?key=${API_CONFIG.fallback.apiKey}&q=${barangay.latitude},${barangay.longitude}`;
          const fallbackResponse = await fetch(fallbackUrl);
          
          if (fallbackResponse.ok) {
            const data = await fallbackResponse.json();
            return {
              name: barangay.name,
              condition: data.current?.condition?.text || 'Unknown',
              temperature: data.current?.temp_c ?? 0,
              time: new Date().toLocaleTimeString('en-PH', { hour: '2-digit', minute: '2-digit', hour12: true })
            };
          }
          
          throw new Error('Both APIs failed');
        } catch (error) {
          console.error(`Error fetching data for ${barangay.name}:`, error);
          return { ...DEFAULT_CITY_RESPONSE, name: barangay.name };
        }
      })
    );
    
    return results;
  } catch (error) {
    console.error('Error in getWeatherDataForPopularCities:', error);
    return barangays.map(barangay => ({ ...DEFAULT_CITY_RESPONSE, name: barangay.name }));
  }
}

function formatCityData(name, data) {
  return {
    name,
    condition: mapWeatherCode(data.current_weather?.weathercode),
    temperature: data.current_weather?.temperature ?? 0,
    time: new Date().toLocaleTimeString('en-PH', { hour: '2-digit', minute: '2-digit', hour12: true })
  };
}