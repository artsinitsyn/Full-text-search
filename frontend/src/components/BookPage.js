import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';
import { Box, Typography, Button } from '@mui/material';

export default function BookPage(){
  const { id } = useParams();
  const [book, setBook] = useState(null);
  useEffect(()=> {
    api.get(`/api/book/${id}/`).then(res=> setBook(res.data)).catch(()=> setBook(null));
  }, [id]);
  if(!book) return <Box p={3}>Loading...</Box>;
  return (
    <Box p={3} maxWidth={900} mx="auto">
      <Button component={Link} to="/" variant="text">← Back to search</Button>
      <Typography variant="h4" gutterBottom dangerouslySetInnerHTML={{__html: book.title}} />
      <Typography variant="subtitle1" color="text.secondary">{book.author} — {book.year}</Typography>
      <Box mt={3}><Typography component="div" sx={{whiteSpace:'pre-wrap'}}>{book.content}</Typography></Box>
    </Box>
  );
}
