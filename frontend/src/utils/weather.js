//   export async function getWeatherData() {
//     const latitude = 13.405165290699628;
//     const longitude = 121.2151274080352;     

//     const response = await fetch(
//         `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true&hourly=temperature_2m,weathercode,relative_humidity_2m,wind_speed_10m,precipitation,precipitation_probability,uv_index,surface_pressure,&daily=temperature_2m_max,temperature_2m_min,weathercode,sunrise,sunset&timezone=auto&forecast_days=10`
//     );      

//     const data = await response.json();
  
//     const now = new Date();
//     const currentHour = now.toISOString().slice(0, 13) + ':00';
//     const currentHourIndex = data.hourly?.time?.findIndex(t => t === currentHour) ?? -1;
  
//     const current = {
//       temperature_c: data.current_weather?.temperature ?? 0,
//       weather_condition: mapWeatherCode(data.current_weather?.weathercode),
//       humidity: data.hourly?.relative_humidity_2m?.[currentHourIndex] ?? 0,
//       wind_speed: data.hourly?.wind_speed_10m?.[currentHourIndex] ?? 0,
//       precipitation: data.hourly?.precipitation?.[currentHourIndex] ?? 0,
//       uv_index: data.hourly?.uv_index?.[currentHourIndex] ?? 0,
//       pressure: data.hourly?.surface_pressure?.[currentHourIndex] ?? 0,
//       wind_direction: data.hourly?.wind_direction_10m?.[currentHourIndex] ?? 0,
//       sunrise: data.daily.sunrise?.[currentHourIndex] ?? '',
//       sunset: data.daily.sunset?.[currentHourIndex] ?? '',
//     };
  
//     const forecast = data.daily?.time?.map((date, index) => ({
//       date,
//       temp: data.daily.temperature_2m_max?.[index] ?? 0,
//       temperature_max: data.daily.temperature_2m_max?.[index] ?? 0,
//       temperature_min: data.daily.temperature_2m_min?.[index] ?? 0,
//       condition_code: data.daily.weathercode?.[index] ?? 0,
//     })) ?? [];
  
//     const hourlyForecast = data.hourly?.time?.slice(0, 10).map((time, index) => ({
//       time: new Date(time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
//       temp: data.hourly.temperature_2m?.[index] ?? 0,
//       condition: mapWeatherCode(data.hourly.weathercode?.[index]),
//       rainChance: data.hourly.precipitation_probability?.[index] ?? 0,
//     })) ?? [];

//     const todayIndex = 0;

//     const sunData = {
//       sunrise: data.daily.sunrise?.[todayIndex] ?? '',
//       sunset: data.daily.sunset?.[todayIndex] ?? '',
//     };

//     const airQuality = {
//         pm2_5: data.hourly?.pm2_5?.[0] ?? 0,
//         pm10: data.hourly?.pm10?.[0] ?? 0,  
//         carbon_monoxide: data.hourly?.carbon_monoxide?.[0] ?? 0, 
//         nitrogen_dioxide: data.hourly?.nitrogen_dioxide?.[0] ?? 0, 
//         ozone: data.hourly?.ozone?.[0] ?? 0,
//         sulphur_dioxide: data.hourly?.sulphur_dioxide?.[0] ?? 0, 
//     };
  
//     return {
//       current,
//       forecast,
//       hourlyForecast,
//       sunData,
//       airQuality,
//     };
//   }

// export async function getWeatherData() {
//     const latitude = 13.405165290699628;
//     const longitude = 121.2151274080352;
  
//     // 1) Fetch weather forecast
//     const weatherRes = await fetch(
//       `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}` +
//       `&current_weather=true` +
//       `&hourly=temperature_2m,weathercode,relative_humidity_2m,wind_speed_10m,wind_direction_10m,precipitation,precipitation_probability,uv_index,surface_pressure` +
//       `&daily=temperature_2m_max,temperature_2m_min,weathercode,sunrise,sunset` +
//       `&timezone=auto&forecast_days=10`
//     );
//     const weatherData = await weatherRes.json();
  
//    // 2) Fetch air quality from the correct endpoint
//     const aqRes = await fetch(
//       `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${latitude}&longitude=${longitude}&hourly=pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide&timezone=auto`
//     );
//     const aqData = await aqRes.json();
  
//     // Compute current hour index
//     const now = new Date();
//     const currentHour = now.toISOString().slice(0, 13) + ':00';
//     let idx = weatherData.hourly?.time?.findIndex(t => t === currentHour) ?? 0;
    
//     // Function to find the most recent non-zero value in an array starting from index
//     const getRecentNonZero = (array, startIndex) => {
//       if (!array) return 0;
      
//       // Check current index first
//       if (array[startIndex] !== undefined && array[startIndex] !== 0) {
//         return array[startIndex];
//       }
      
//       // Search backwards for the most recent non-zero value
//       for (let i = startIndex - 1; i >= 0; i--) {
//         if (array[i] !== undefined && array[i] !== 0) {
//           return array[i];
//         }
//       }
      
//       // If no non-zero found, search forwards
//       for (let i = startIndex + 1; i < array.length; i++) {
//         if (array[i] !== undefined && array[i] !== 0) {
//           return array[i];
//         }
//       }
      
//       // If still nothing found, return 0
//       return 0;
//     };
  
//     // Build current summary with fallback to recent non-zero data
//     const current = {
//       temperature_c: weatherData.current_weather?.temperature ?? 
//                    getRecentNonZero(weatherData.hourly?.temperature_2m, idx),
//       weather_condition: mapWeatherCode(weatherData.current_weather?.weathercode),
//       humidity: getRecentNonZero(weatherData.hourly?.relative_humidity_2m, idx),
//       wind_speed: getRecentNonZero(weatherData.hourly?.wind_speed_10m, idx),
//       wind_direction: getRecentNonZero(weatherData.hourly?.wind_direction_10m, idx),
//       precipitation: getRecentNonZero(weatherData.hourly?.precipitation, idx),
//       rainChance: getRecentNonZero(weatherData.hourly?.precipitation_probability, idx),
//       uv_index: getRecentNonZero(weatherData.hourly?.uv_index, idx),
//       pressure: getRecentNonZero(weatherData.hourly?.surface_pressure, idx),
//       sunrise: weatherData.daily?.sunrise?.[0] ?? '',
//       sunset: weatherData.daily?.sunset?.[0] ?? '',
//     };
  
//     // 7- or 10-day daily forecast
//     const forecast = weatherData.daily?.time?.map((date, i) => ({
//       date,
//       temperature_max: weatherData.daily.temperature_2m_max?.[i] ?? 0,
//       temperature_min: weatherData.daily.temperature_2m_min?.[i] ?? 0,
//       condition_code: weatherData.daily.weathercode?.[i] ?? 0,
//     })) ?? [];
  
//     // Next 10 hours for chart
//     const hourlyForecast = weatherData.hourly?.time?.slice(0, 10).map((t, i) => ({
//       time: new Date(t).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
//       temp: weatherData.hourly.temperature_2m?.[i] ?? 0,
//       condition: mapWeatherCode(weatherData.hourly.weathercode?.[i]),
//       rainChance: weatherData.hourly.precipitation_probability?.[i] ?? 0,
//     })) ?? [];
  
//     // Air quality hour 0
//     const airQuality = {
//       pm2_5: aqData.hourly?.pm2_5?.[0] ?? 0,
//       pm10: aqData.hourly?.pm10?.[0] ?? 0,
//       carbon_monoxide: aqData.hourly?.carbon_monoxide?.[0] ?? 0,
//       nitrogen_dioxide: aqData.hourly?.nitrogen_dioxide?.[0] ?? 0,
//       ozone: aqData.hourly?.ozone?.[0] ?? 0,
//       sulphur_dioxide: aqData.hourly?.sulphur_dioxide?.[0] ?? 0,
//     };

//     const todayIndex = 0;

//     const sunData = {
//         sunrise: weatherData.daily.sunrise?.[todayIndex] ?? '',
//         sunset: weatherData.daily.sunset?.[todayIndex] ?? '',
//     };
  
//     return {
//       current,
//       forecast,
//       hourlyForecast,
//       airQuality,
//       sunData
//     };
// }

// // ... rest of your code (getWeatherDataForPopularCities and mapWeatherCode) remains the same ...

// export async function getWeatherDataForPopularCities() {
//     const barangays = [
//         { name: 'Bulusan', latitude: 13.4037, longitude: 121.2012 },
//         { name: 'Suqui', latitude: 13.4177, longitude: 121.2040 },
//         { name: 'Santo Niño', latitude: 13.4066, longitude: 121.1848 },
//         { name: 'Ilaya (Poblacion)', latitude: 13.4129, longitude: 121.1840 },
//         { name: 'Silonay', latitude: 13.3992, longitude: 121.2248 }
//     ];
  
//     const results = await Promise.all(
//     barangays.map(async (barangay) => {
//       const url = `https://api.open-meteo.com/v1/forecast?latitude=${barangay.latitude}&longitude=${barangay.longitude}&current_weather=true&timezone=auto`;

//       const response = await fetch(url);
//       const data = await response.json();

//       const condition = mapWeatherCode(data.current_weather?.weathercode);
//       const temperature = data.current_weather?.temperature ?? 0;
//       const now = new Date();
//       const localTime = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

//       return {
//         name: barangay.name,
//         condition,
//         temperature,
//         time: localTime
//       };
//     })
//   );
  
//     return results;
// }
  
// export function mapWeatherCode(code) {
//     const mapping = {
//         0: 'Clear',
//         1: 'Mainly Clear',
//         2: 'Partly Cloudy',
//         3: 'Overcast',
//         45: 'Fog',
//         48: 'Depositing Rime Fog',
//         51: 'Light Drizzle',
//         53: 'Moderate Drizzle',
//         55: 'Dense Drizzle',
//         61: 'Light Rain',
//         63: 'Moderate Rain',
//         65: 'Heavy Rain',
//         66: 'Freezing Rain',
//         67: 'Heavy Freezing Rain',
//         71: 'Light Snowfall',
//         73: 'Moderate Snowfall',
//         75: 'Heavy Snowfall',
//         80: 'Rain Showers',
//         81: 'Heavy Rain Showers',
//         82: 'Violent Rain Showers',
//         95: 'Thunderstorm',
//         96: 'Thunderstorm with Hail',
//         99: 'Severe Thunderstorm',
//     };
//     return mapping[code] || 'Unknown';
// }

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
    apiKey: 'be2785e8e2f44f11b2605501251508' // You'll need to sign up for a free key
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

// Helper functions
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

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

// API Fetch Functions
async function fetchWithFallback(url, options = {}, fallbackUrl, fallbackOptions = {}) {
  try {
    const response = await fetch(url, options);
    if (response.ok) return await response.json();
    throw new Error(`Primary API failed with status ${response.status}`);
  } catch (primaryError) {
    console.warn('Primary API failed, trying fallback:', primaryError.message);
    try {
      const fallbackResponse = await fetch(fallbackUrl, fallbackOptions);
      if (!fallbackResponse.ok) throw new Error(`Fallback API failed with status ${fallbackResponse.status}`);
      return await fallbackResponse.json();
    } catch (fallbackError) {
      console.error('Both APIs failed:', fallbackError.message);
      throw fallbackError;
    }
  }
}

// Data Processing Functions
function processOpenMeteoData(weatherData, aqData) {
  const now = new Date();
  const currentHour = now.toISOString().slice(0, 13) + ':00';
  const idx = weatherData.hourly?.time?.findIndex(t => t === currentHour) ?? 0;
  const todayIndex = 0;

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
    hourlyForecast: weatherData.hourly?.time?.slice(0, 10).map((t, i) => ({
      time: new Date(t).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      temp: weatherData.hourly.temperature_2m?.[i] ?? 0,
      condition: mapWeatherCode(weatherData.hourly.weathercode?.[i]),
      rainChance: weatherData.hourly.precipitation_probability?.[i] ?? 0,
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
      sunrise: weatherData.daily?.sunrise?.[todayIndex] ?? '06:00',
      sunset: weatherData.daily?.sunset?.[todayIndex] ?? '18:00',
    }
  };
}

function processWeatherApiData(data) {
  const current = data.current;
  const forecast = data.forecast?.forecastday?.[0]?.hour || [];
  
  return {
    current: {
      temperature_c: current?.temp_c ?? 0,
      weather_condition: current?.condition?.text || 'Unknown',
      humidity: current?.humidity ?? 0,
      wind_speed: current?.wind_kph ?? 0,
      wind_direction: current?.wind_degree ?? 0,
      precipitation: current?.precip_mm ?? 0,
      rainChance: forecast[0]?.chance_of_rain ?? 0,
      uv_index: current?.uv ?? 0,
      pressure: current?.pressure_mb ?? 0,
      sunrise: data.forecast?.forecastday?.[0]?.astro?.sunrise || '06:00',
      sunset: data.forecast?.forecastday?.[0]?.astro?.sunset || '18:00',
    },
    forecast: data.forecast?.forecastday?.map(day => ({
      date: day.date,
      temperature_max: day.day?.maxtemp_c ?? 0,
      temperature_min: day.day?.mintemp_c ?? 0,
      condition_code: mapWeatherCodeFromText(day.day?.condition?.text),
    })) || DEFAULT_RESPONSE.forecast,
    hourlyForecast: forecast.slice(0, 10).map(hour => ({
      time: hour.time.split(' ')[1],
      temp: hour.temp_c ?? 0,
      condition: hour.condition?.text || 'Unknown',
      rainChance: hour.chance_of_rain ?? 0,
    })) || DEFAULT_RESPONSE.hourlyForecast,
    airQuality: DEFAULT_RESPONSE.airQuality, // WeatherAPI.com doesn't provide air quality in free tier
    sunData: {
      sunrise: data.forecast?.forecastday?.[0]?.astro?.sunrise || '06:00',
      sunset: data.forecast?.forecastday?.[0]?.astro?.sunset || '18:00',
    }
  };
}

// Main Weather Data Function
export async function getWeatherData() {
  try {
    // Try primary API (Open-Meteo) first
    try {
      const [weatherData, aqData] = await Promise.all([
        fetch(`${API_CONFIG.primary.baseUrl}${API_CONFIG.primary.endpoints.forecast}?latitude=${DEFAULT_LOCATION.latitude}&longitude=${DEFAULT_LOCATION.longitude}&current_weather=true&hourly=temperature_2m,weathercode,relative_humidity_2m,wind_speed_10m,wind_direction_10m,precipitation,precipitation_probability,uv_index,surface_pressure&daily=temperature_2m_max,temperature_2m_min,weathercode,sunrise,sunset&timezone=auto&forecast_days=10`)
          .then(r => r.ok ? r.json() : Promise.reject(new Error(`Status ${r.status}`))),
        
        fetch(`${API_CONFIG.primary.aqBaseUrl}${API_CONFIG.primary.endpoints.airQuality}?latitude=${DEFAULT_LOCATION.latitude}&longitude=${DEFAULT_LOCATION.longitude}&hourly=pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide&timezone=auto`)
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

// Weather Code Mapping (Extended for both APIs)
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
          const primaryUrl = `${API_CONFIG.primary.baseUrl}${API_CONFIG.primary.endpoints.forecast}?latitude=${barangay.latitude}&longitude=${barangay.longitude}&current_weather=true&timezone=auto`;
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
              time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
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
    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  };
}