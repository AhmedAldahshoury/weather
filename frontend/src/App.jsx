import React, { useState } from 'react';
import { Block } from 'baseui/block';
import { Heading, HeadingLevel } from 'baseui/heading';
import { Input } from 'baseui/input';
import { Button } from 'baseui/button';
import { Card } from 'baseui/card';
import { ParagraphMedium } from 'baseui/typography';

function App() {
  const [cityName, setCityName] = useState('');
  const [forecastData, setForecastData] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!cityName) return;
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`http://localhost:5000/forecast/city/${encodeURIComponent(cityName)}`);
      const data = await response.json();
      if (response.ok) {
        setForecastData(data.forecasts);
      } else {
        setError(data.error || 'Error fetching data.');
        setForecastData([]);
      }
    } catch (e) {
      setError('Error fetching data.');
      setForecastData([]);
    }
    setLoading(false);
  };

  return (
    <Block backgroundColor="#f0f4f8" minHeight="100vh" padding="scale800">
      {/* Header */}
      <Block display="flex" flexDirection="column" alignItems="center" marginBottom="scale800">
        <HeadingLevel>
          <Heading styleLevel={1}>Weather Forecast</Heading>
        </HeadingLevel>
        <Block marginTop="scale600" width={['100%', '80%', '60%']}>
          {/* Remove or set clearable={false} to avoid the “X” icon */}
          <Input
            value={cityName}
            placeholder="Enter a city name"
            onChange={(e) => setCityName(e.target.value)}
          />
        </Block>
        <Block marginTop="scale400">
          <Button onClick={handleSearch}>Search</Button>
        </Block>
      </Block>

      {/* Error Message */}
      {error && (
        <Block marginBottom="scale600" color="negative">
          {error}
        </Block>
      )}

      {/* Forecast Cards */}
      {loading ? (
        <Block>Loading...</Block>
      ) : (
        <Block display="flex" flexWrap="wrap" gridGap="scale600" justifyContent="center">
          {forecastData.length > 0 ? (
            forecastData.map((forecast, index) => (
              <Card key={index} overrides={{ Root: { style: { width: '300px' } } }}>
                <Block padding="scale300">
                  <HeadingLevel>
                    <Heading styleLevel={4}>{forecast.date}</Heading>
                  </HeadingLevel>
                  <ParagraphMedium>Temperature: {forecast.temperature}°C</ParagraphMedium>
                  <ParagraphMedium>Humidity: {forecast.humidity}%</ParagraphMedium>
                  <ParagraphMedium>Condition: {forecast.condition}</ParagraphMedium>
                  <ParagraphMedium>Wind Speed: {forecast.wind_speed} km/h</ParagraphMedium>
                </Block>
              </Card>
            ))
          ) : (
            <Block>Enter a city name and click "Search" to view the forecast.</Block>
          )}
        </Block>
      )}
    </Block>
  );
}

export default App;
