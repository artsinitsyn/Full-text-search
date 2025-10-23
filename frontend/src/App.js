import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Search from './components/Search';
import BookPage from './components/BookPage';
import { AppBar, Toolbar, Typography } from '@mui/material';

export default function App(){
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">Library Explorer</Typography>
        </Toolbar>
      </AppBar>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Search />} />
          <Route path="/book/:id" element={<BookPage />} />
        </Routes>
      </BrowserRouter>
    </>
  );
}
