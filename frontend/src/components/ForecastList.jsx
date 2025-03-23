import React, { useState, useEffect } from 'react';
import { FormControl } from 'baseui/form-control';
import { Input } from 'baseui/input';
import { Button } from 'baseui/button';
import { Card } from 'baseui/card';
import { Select } from 'baseui/select';
import { Modal, ModalHeader, ModalBody, ModalFooter, ModalButton } from 'baseui/modal';
import { Block } from 'baseui/block';

function ForecastList() {
  const [forecasts, setForecasts] = useState([]);
  const [cities, setCities] = useState([]);
  const [selectedCity, setSelectedCity] = useState(null);
  const [date, setDate] = useState('');
  const [temperature, setTemperature] = useState('');
  const [humidity, setHumidity] = useState('');
  const [condition, setCondition] = useState('');
  const [windSpeed, setWindSpeed] = useState('');
  const [message, setMessage] = useState('');
  const [editForecast, setEditForecast] = useState(null);
  const [editDate, setEditDate] = useState('');
  const [editTemperature, setEditTemperature] = useState('');
  const [editHumidity, setEditHumidity] = useState('');
  const [editCondition, setEditCondition] = useState('');
  const [editWindSpeed, setEditWindSpeed] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchCities();
  }, []);

  const fetchCities = async () => {
    try {
      const response = await fetch('http://localhost:5000/city');
      const data = await response.json();
      const options = data.cities.map(city => ({ id: city.id, label: city.name }));
      setCities(options);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchForecasts = async (cityName) => {
    try {
      const response = await fetch(`http://localhost:5000/forecast/city/${cityName}`);
      const data = await response.json();
      setForecasts(data.forecasts);
    } catch (error) {
      console.error(error);
    }
  };

  const handleCitySelect = ({ value }) => {
    if (value.length > 0) {
      const city = value[0];
      setSelectedCity(city);
      fetchForecasts(city.label);
    }
  };

  const handleAddForecast = async () => {
    if (!selectedCity) {
      setMessage("Please select a city first.");
      return;
    }
    const payload = {
      city_name: selectedCity.label,
      date,
      temperature: parseFloat(temperature),
      humidity: parseFloat(humidity),
      condition,
      wind_speed: parseFloat(windSpeed)
    };
    try {
      const response = await fetch('http://localhost:5000/forecast', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(data.message);
        // Reset input fields
        setDate('');
        setTemperature('');
        setHumidity('');
        setCondition('');
        setWindSpeed('');
        // Reload forecasts
        fetchForecasts(selectedCity.label);
      } else {
        setMessage(data.error);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleDeleteForecast = async (forecastId) => {
    try {
      const response = await fetch(`http://localhost:5000/forecast/${forecastId}`, {
        method: 'DELETE'
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(data.message);
        fetchForecasts(selectedCity.label);
      } else {
        setMessage(data.error);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const openEditModal = (forecast) => {
    setEditForecast(forecast);
    setEditDate(forecast.date);
    setEditTemperature(forecast.temperature);
    setEditHumidity(forecast.humidity);
    setEditCondition(forecast.condition);
    setEditWindSpeed(forecast.wind_speed);
    setIsModalOpen(true);
  };

  const handleUpdateForecast = async () => {
    if (!editForecast) return;
    const payload = {
      temperature: parseFloat(editTemperature),
      humidity: parseFloat(editHumidity),
      condition: editCondition,
      wind_speed: parseFloat(editWindSpeed)
    };
    try {
      const response = await fetch(`http://localhost:5000/forecast/${editForecast.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(data.message);
        fetchForecasts(selectedCity.label);
      } else {
        setMessage(data.error);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsModalOpen(false);
      setEditForecast(null);
    }
  };

  return (
    <Block padding="scale800">
      <Block as="h2" marginBottom="scale600">Manage Forecasts</Block>

      {message && (
        <Block marginBottom="scale400" color="primary">
          {message}
        </Block>
      )}

      {/* City Selection */}
      <Block marginBottom="scale600">
        <FormControl label="Select City">
          <Select
            options={cities}
            onChange={handleCitySelect}
            value={selectedCity ? [selectedCity] : []}
            // Remove all icons
            clearable={false}
            overrides={{
              SelectArrow: {
                style: {
                  display: 'none', // Hide dropdown arrow
                },
              },
            }}
          />
        </FormControl>
      </Block>

      {/* Add Forecast Form */}
      <Block display="flex" flexWrap="wrap" alignItems="center" marginBottom="scale600">
        <Block flex="1" marginRight="scale400">
          <FormControl label="Date">
            <Input
              value={date}
              type="date"
              onChange={(e) => setDate(e.target.value)}
            />
          </FormControl>
        </Block>
        <Block flex="1" marginRight="scale400">
          <FormControl label="Temperature">
            <Input
              value={temperature}
              type="number"
              onChange={(e) => setTemperature(e.target.value)}
            />
          </FormControl>
        </Block>
      </Block>

      <Block display="flex" flexWrap="wrap" alignItems="center" marginBottom="scale600">
        <Block flex="1" marginRight="scale400">
          <FormControl label="Humidity">
            <Input
              value={humidity}
              type="number"
              onChange={(e) => setHumidity(e.target.value)}
            />
          </FormControl>
        </Block>
        <Block flex="1" marginRight="scale400">
          <FormControl label="Condition">
            <Input
              value={condition}
              onChange={(e) => setCondition(e.target.value)}
            />
          </FormControl>
        </Block>
        <Block flex="1" marginRight="scale400">
          <FormControl label="Wind Speed">
            <Input
              value={windSpeed}
              type="number"
              onChange={(e) => setWindSpeed(e.target.value)}
            />
          </FormControl>
        </Block>
        <Button onClick={handleAddForecast}>Add Forecast</Button>
      </Block>

      {/* Forecast Cards */}
      <Block display="flex" flexWrap="wrap" gridGap="scale600">
        {forecasts.map((forecast) => (
          <Card
            key={forecast.id}
            overrides={{
              Root: { style: { width: '300px', marginBottom: '20px' } },
            }}
          >
            <Block padding="scale300">
              <Block font="font600" marginBottom="scale200">
                Date: {forecast.date}
              </Block>
              <Block marginBottom="scale200">
                Temp: {forecast.temperature}°C | Humidity: {forecast.humidity}%
              </Block>
              <Block marginBottom="scale200">
                Condition: {forecast.condition} | Wind: {forecast.wind_speed} km/h
              </Block>
              <Block display="flex">
                <Button
                  onClick={() => openEditModal(forecast)}
                  size="mini"
                  overrides={{ BaseButton: { style: { marginRight: '8px' } } }}
                >
                  Update
                </Button>
                <Button onClick={() => handleDeleteForecast(forecast.id)} size="mini" kind="secondary">
                  Delete
                </Button>
              </Block>
            </Block>
          </Card>
        ))}
      </Block>

      {/* Edit Forecast Modal */}
      <Modal
        onClose={() => setIsModalOpen(false)}
        isOpen={isModalOpen}
        closeable={false} // No "X" icon in the corner
      >
        <ModalHeader>Update Forecast</ModalHeader>
        <ModalBody>
          <FormControl label="Date">
            <Input
              value={editDate}
              type="date"
              onChange={(e) => setEditDate(e.target.value)}
            />
          </FormControl>
          <FormControl label="Temperature">
            <Input
              value={editTemperature}
              type="number"
              onChange={(e) => setEditTemperature(e.target.value)}
            />
          </FormControl>
          <FormControl label="Humidity">
            <Input
              value={editHumidity}
              type="number"
              onChange={(e) => setEditHumidity(e.target.value)}
            />
          </FormControl>
          <FormControl label="Condition">
            <Input
              value={editCondition}
              onChange={(e) => setEditCondition(e.target.value)}
            />
          </FormControl>
          <FormControl label="Wind Speed">
            <Input
              value={editWindSpeed}
              type="number"
              onChange={(e) => setEditWindSpeed(e.target.value)}
            />
          </FormControl>
        </ModalBody>
        <ModalFooter>
          <ModalButton kind="tertiary" onClick={() => setIsModalOpen(false)}>Cancel</ModalButton>
          <ModalButton onClick={handleUpdateForecast}>Update</ModalButton>
        </ModalFooter>
      </Modal>
    </Block>
  );
}

export default ForecastList;
