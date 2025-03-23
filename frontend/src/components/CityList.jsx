import React, { useState, useEffect } from 'react';
import { FormControl } from 'baseui/form-control';
import { Input } from 'baseui/input';
import { Button } from 'baseui/button';
import { Card } from 'baseui/card';
import { Modal, ModalHeader, ModalBody, ModalFooter, ModalButton } from 'baseui/modal';
import { Block } from 'baseui/block';

function CityList() {
  const [cities, setCities] = useState([]);
  const [name, setName] = useState('');
  const [country, setCountry] = useState('');
  const [message, setMessage] = useState('');
  const [editCity, setEditCity] = useState(null);
  const [editName, setEditName] = useState('');
  const [editCountry, setEditCountry] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchCities();
  }, []);

  const fetchCities = async () => {
    try {
      const response = await fetch('http://localhost:5000/city');
      const data = await response.json();
      setCities(data.cities);
    } catch (error) {
      console.error(error);
    }
  };

  const handleAddCity = async () => {
    const payload = { name, country };
    try {
      const response = await fetch('http://localhost:5000/city', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(data.message);
        setName('');
        setCountry('');
        fetchCities();
      } else {
        setMessage(data.error);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const handleDeleteCity = async (id) => {
    try {
      const response = await fetch(`http://localhost:5000/city/${id}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(data.message);
        fetchCities();
      } else {
        setMessage(data.error);
      }
    } catch (error) {
      console.error(error);
    }
  };

  const openEditModal = (city) => {
    setEditCity(city);
    setEditName(city.name);
    setEditCountry(city.country);
    setIsModalOpen(true);
  };

  const handleUpdateCity = async () => {
    if (!editCity) return;
    const payload = { name: editName, country: editCountry };
    try {
      const response = await fetch(`http://localhost:5000/city/${editCity.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (response.ok) {
        setMessage(data.message);
        fetchCities();
      } else {
        setMessage(data.error);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setIsModalOpen(false);
      setEditCity(null);
    }
  };

  return (
    <Block padding="scale800">
      <Block as="h2" marginBottom="scale600">
        Manage Cities
      </Block>
      {message && (
        <Block marginBottom="scale400" color="primary">
          {message}
        </Block>
      )}

      {/* Add City Form */}
      <Block display="flex" flexWrap="wrap" alignItems="center" marginBottom="scale600">
        <Block flex="1" marginRight="scale400">
          <FormControl label="City Name">
            {/* clearable is removed */}
            <Input
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </FormControl>
        </Block>
        <Block flex="1" marginRight="scale400">
          <FormControl label="Country">
            {/* clearable is removed */}
            <Input
              value={country}
              onChange={(e) => setCountry(e.target.value)}
            />
          </FormControl>
        </Block>
        <Button onClick={handleAddCity}>Add City</Button>
      </Block>

      {/* City Cards */}
      <Block display="flex" flexWrap="wrap" gridGap="scale600">
        {cities.map((city) => (
          <Card
            key={city.id}
            overrides={{
              Root: { style: { width: '300px', marginBottom: '20px', cursor: 'pointer' } },
            }}
          >
            <Block padding="scale300">
              <Block font="font600" marginBottom="scale200">
                {city.name} - {city.country}
              </Block>
              <Block marginBottom="scale200">
                Lat: {city.latitude} | Long: {city.longitude}
              </Block>
              <Block display="flex">
                <Button
                  onClick={() => openEditModal(city)}
                  size="mini"
                  overrides={{ BaseButton: { style: { marginRight: '8px' } } }}
                >
                  Update
                </Button>
                <Button onClick={() => handleDeleteCity(city.id)} size="mini" kind="secondary">
                  Delete
                </Button>
              </Block>
            </Block>
          </Card>
        ))}
      </Block>

      {/* Edit City Modal */}
      <Modal
        onClose={() => setIsModalOpen(false)}
        isOpen={isModalOpen}
        // This removes the top-right close "X"
        closeable={false}
      >
        <ModalHeader>Update City</ModalHeader>
        <ModalBody>
          <FormControl label="City Name">
            <Input
              value={editName}
              onChange={(e) => setEditName(e.target.value)}
            />
          </FormControl>
          <FormControl label="Country">
            <Input
              value={editCountry}
              onChange={(e) => setEditCountry(e.target.value)}
            />
          </FormControl>
        </ModalBody>
        <ModalFooter>
          <ModalButton kind="tertiary" onClick={() => setIsModalOpen(false)}>
            Cancel
          </ModalButton>
          <ModalButton onClick={handleUpdateCity}>Update</ModalButton>
        </ModalFooter>
      </Modal>
    </Block>
  );
}

export default CityList;
