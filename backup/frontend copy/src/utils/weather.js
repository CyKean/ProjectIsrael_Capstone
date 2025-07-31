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

export async function getWeatherData() {
    const latitude = 13.405165290699628;
    const longitude = 121.2151274080352;
  
    // 1) Fetch weather forecast
    const weatherRes = await fetch(
      `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}` +
      `&current_weather=true` +
      `&hourly=temperature_2m,weathercode,relative_humidity_2m,wind_speed_10m,wind_direction_10m,precipitation,precipitation_probability,uv_index,surface_pressure` +
      `&daily=temperature_2m_max,temperature_2m_min,weathercode,sunrise,sunset` +
      `&timezone=auto&forecast_days=10`
    );
    const weatherData = await weatherRes.json();
  
   // 2) Fetch air quality from the correct endpoint
    const aqRes = await fetch(
      `https://air-quality-api.open-meteo.com/v1/air-quality?latitude=${latitude}&longitude=${longitude}&hourly=pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,ozone,sulphur_dioxide&timezone=auto`
    );
    const aqData = await aqRes.json();
  
    // Compute current hour index
    const now = new Date();
    const currentHour = now.toISOString().slice(0, 13) + ':00';
    let idx = weatherData.hourly?.time?.findIndex(t => t === currentHour) ?? 0;
    
    // Function to find the most recent non-zero value in an array starting from index
    const getRecentNonZero = (array, startIndex) => {
      if (!array) return 0;
      
      // Check current index first
      if (array[startIndex] !== undefined && array[startIndex] !== 0) {
        return array[startIndex];
      }
      
      // Search backwards for the most recent non-zero value
      for (let i = startIndex - 1; i >= 0; i--) {
        if (array[i] !== undefined && array[i] !== 0) {
          return array[i];
        }
      }
      
      // If no non-zero found, search forwards
      for (let i = startIndex + 1; i < array.length; i++) {
        if (array[i] !== undefined && array[i] !== 0) {
          return array[i];
        }
      }
      
      // If still nothing found, return 0
      return 0;
    };
  
    // Build current summary with fallback to recent non-zero data
    const current = {
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
      sunrise: weatherData.daily?.sunrise?.[0] ?? '',
      sunset: weatherData.daily?.sunset?.[0] ?? '',
    };
  
    // 7- or 10-day daily forecast
    const forecast = weatherData.daily?.time?.map((date, i) => ({
      date,
      temperature_max: weatherData.daily.temperature_2m_max?.[i] ?? 0,
      temperature_min: weatherData.daily.temperature_2m_min?.[i] ?? 0,
      condition_code: weatherData.daily.weathercode?.[i] ?? 0,
    })) ?? [];
  
    // Next 10 hours for chart
    const hourlyForecast = weatherData.hourly?.time?.slice(0, 10).map((t, i) => ({
      time: new Date(t).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      temp: weatherData.hourly.temperature_2m?.[i] ?? 0,
      condition: mapWeatherCode(weatherData.hourly.weathercode?.[i]),
      rainChance: weatherData.hourly.precipitation_probability?.[i] ?? 0,
    })) ?? [];
  
    // Air quality hour 0
    const airQuality = {
      pm2_5: aqData.hourly?.pm2_5?.[0] ?? 0,
      pm10: aqData.hourly?.pm10?.[0] ?? 0,
      carbon_monoxide: aqData.hourly?.carbon_monoxide?.[0] ?? 0,
      nitrogen_dioxide: aqData.hourly?.nitrogen_dioxide?.[0] ?? 0,
      ozone: aqData.hourly?.ozone?.[0] ?? 0,
      sulphur_dioxide: aqData.hourly?.sulphur_dioxide?.[0] ?? 0,
    };

    const todayIndex = 0;

    const sunData = {
        sunrise: weatherData.daily.sunrise?.[todayIndex] ?? '',
        sunset: weatherData.daily.sunset?.[todayIndex] ?? '',
    };
  
    return {
      current,
      forecast,
      hourlyForecast,
      airQuality,
      sunData
    };
}

// ... rest of your code (getWeatherDataForPopularCities and mapWeatherCode) remains the same ...

export async function getWeatherDataForPopularCities() {
    const barangays = [
        { name: 'Bulusan', latitude: 13.4037, longitude: 121.2012 },
        { name: 'Suqui', latitude: 13.4177, longitude: 121.2040 },
        { name: 'Santo Niño', latitude: 13.4066, longitude: 121.1848 },
        { name: 'Ilaya (Poblacion)', latitude: 13.4129, longitude: 121.1840 },
        { name: 'Silonay', latitude: 13.3992, longitude: 121.2248 }
    ];
  
    const results = await Promise.all(
    barangays.map(async (barangay) => {
      const url = `https://api.open-meteo.com/v1/forecast?latitude=${barangay.latitude}&longitude=${barangay.longitude}&current_weather=true&timezone=auto`;

      const response = await fetch(url);
      const data = await response.json();

      const condition = mapWeatherCode(data.current_weather?.weathercode);
      const temperature = data.current_weather?.temperature ?? 0;
      const now = new Date();
      const localTime = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      return {
        name: barangay.name,
        condition,
        temperature,
        time: localTime
      };
    })
  );
  
    return results;
}
  
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