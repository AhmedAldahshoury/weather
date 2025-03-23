import React, { useState } from 'react';
import { Block } from 'baseui/block';
import { Heading, HeadingLevel } from 'baseui/heading';
import { Input } from 'baseui/input';
import { Button } from 'baseui/button';
import { Card } from 'baseui/card';
import { ParagraphMedium } from 'baseui/typography';

function App() {
  // Existing states for forecast search
  const [cityName, setCityName] = useState('');
  const [forecastData, setForecastData] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // New states for adding a city
  const [cityNameToAdd, setCityNameToAdd] = useState('');
  const [countryToAdd, setCountryToAdd] = useState('');
  const [addCityMessage, setAddCityMessage] = useState('');

  // Handle forecast search
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

  // Handle adding a new city
  const handleAddCity = async () => {
    if (!cityNameToAdd || !countryToAdd) return;
    setAddCityMessage(''); // clear any old messages

    try {
      const response = await fetch('http://localhost:5000/city', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: cityNameToAdd, country: countryToAdd }),
      });
      const data = await response.json();

      if (response.ok) {
        setAddCityMessage(data.message || 'City added successfully!');
        // Clear inputs
        setCityNameToAdd('');
        setCountryToAdd('');
      } else {
        setAddCityMessage(data.error || 'Error adding city.');
      }
    } catch (error) {
      setAddCityMessage('Error adding city.');
    }
  };

  return (
    <Block backgroundColor="#f0f4f8" minHeight="100vh" padding="scale800">
      {/* Header / Forecast Search */}
      <Block display="flex" flexDirection="column" alignItems="center" marginBottom="scale800">
        <HeadingLevel>
          <Heading styleLevel={1}>Weather Forecast</Heading>
        </HeadingLevel>

        {/* Search for forecast */}
        <Block marginTop="scale600" width={['100%', '80%', '60%']}>
          <Input
            value={cityName}
            placeholder="Enter a city name to get the forecast"
            onChange={(e) => setCityName(e.target.value)}
            // No 'clearable' to avoid the "X" icon
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

      {/* Add New City Section */}
      <Block marginTop="scale800">
        <HeadingLevel>
          <Heading styleLevel={3}>Add a New City</Heading>
        </HeadingLevel>
        <Block
          marginTop="scale600"
          width={['100%', '80%', '60%']}
          display="flex"
          flexDirection="column"
          gridGap="scale400"
        >
          <Input
            value={cityNameToAdd}
            placeholder="City Name"
            onChange={(e) => setCityNameToAdd(e.target.value)}
          />
          <Input
            value={countryToAdd}
            placeholder="Country"
            onChange={(e) => setCountryToAdd(e.target.value)}
          />
          <Button onClick={handleAddCity}>Add City</Button>

          {addCityMessage && (
            <Block color="primary" marginTop="scale400">
              {addCityMessage}
            </Block>
          )}
        </Block>
      </Block>
    </Block>
  );
}

export default App;
