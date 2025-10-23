import React, { useState, useEffect, useCallback } from "react";
import {
  Box, TextField, Grid, Card, CardContent,
  Typography, FormControl, InputLabel,
  Select, MenuItem, Slider, Pagination, Button, Stack, CircularProgress, Checkbox, ListItemText
} from "@mui/material";
import api from "../api";
import { Link } from "react-router-dom";

export default function Search(){
  const [q, setQ] = useState("");
  const [results, setResults] = useState([]);
  const [genres, setGenres] = useState([]);
  const [selectedGenres, setSelectedGenres] = useState([]);
  const [yearRange, setYearRange] = useState([1800, 2025]);
  const [page, setPage] = useState(1);
  const [size] = useState(10);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);

  const fetchData = useCallback(async (opts={})=>{
    setLoading(true);
    try{
      const params = new URLSearchParams();
      if (opts.q !== undefined ? opts.q : q) params.append('q', opts.q !== undefined ? opts.q : q);
      (opts.genres !== undefined ? opts.genres : selectedGenres).forEach(g => params.append('genre', g));
      const yr = opts.yearRange !== undefined ? opts.yearRange : yearRange;
      if (yr && yr.length===2){ params.append('year_from', yr[0]); params.append('year_to', yr[1]); }
      params.append('page', opts.page || page);
      params.append('size', size);

      const res = await api.get('/api/search?' + params.toString());
      const data = res.data || {};

      setResults(data.hits || []);
      setTotal(data.total || 0);

      const aggs = data.aggs || {};
      if (aggs.genres && aggs.genres.buckets)
        setGenres(aggs.genres.buckets.map(b => b.key));
      else
        setGenres([]);

    }catch(e){
      console.error(e);
    }finally{
      setLoading(false);
    }
  }, [q, selectedGenres, yearRange, page, size]);

  useEffect(()=>{ fetchData(); }, [fetchData]);

  const onApply = ()=>{
    setPage(1);
    fetchData({ q, genres: selectedGenres, yearRange, page:1 });
  };

  return (
    <Box sx={{ display:'flex', p:2 }}>
      <Box sx={{ width:280, mr:3, border:1, borderColor:'divider', borderRadius:2, p:2 }}>
        <Typography variant="h6">Filters</Typography>

        <FormControl fullWidth sx={{ mt:2 }}>
          <InputLabel>Genres</InputLabel>
          <Select
            multiple
            value={selectedGenres}
            onChange={(e)=>setSelectedGenres(e.target.value)}
            renderValue={(v)=>v.join(', ')}>
            {genres.map(g=>(
              <MenuItem key={g} value={g}>
                <Checkbox checked={selectedGenres.includes(g)} />
                <ListItemText primary={g} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Box sx={{ mt:3 }}>
          <Typography gutterBottom>Years</Typography>
          <Slider
            value={yearRange}
            min={1600}
            max={2025}
            onChange={(e,v)=>setYearRange(v)}
            valueLabelDisplay="auto"
          />
        </Box>

        <TextField
          label="Query"
          fullWidth sx={{ mt:2 }}
          value={q}
          onChange={e=>setQ(e.target.value)}
          onKeyDown={e=>{ if(e.key==='Enter') onApply(); }}
        />

        <Stack direction="row" spacing={1} sx={{ mt:2 }}>
          <Button variant="contained" onClick={onApply}>Apply</Button>
          <Button variant="outlined" onClick={()=>{
            setSelectedGenres([]);
            setYearRange([1800,2025]);
            setQ('');
            setPage(1);
            fetchData({ q:'', genres:[], yearRange:[1800,2025], page:1 });
          }}>Reset</Button>
        </Stack>
      </Box>

      <Box sx={{ flex:1 }}>
        {loading ? (
          <Box sx={{ display:'flex', justifyContent:'center', p:4 }}>
            <CircularProgress/>
          </Box>
        ) : null}

        <Typography variant="subtitle1" gutterBottom>{total} results</Typography>

        <Grid container spacing={2}>
          {results.map(b=>(
            <Grid item xs={12} key={b.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6" dangerouslySetInnerHTML={{ __html: b.highlight?.title?.[0] || b.title }} />
                  <Typography variant="body2" color="text.secondary">
                    {b.author} — {b.year}
                  </Typography>
                  <Box sx={{ mt:1 }}>
                    <Typography component="div"
                      dangerouslySetInnerHTML={{
                        __html: b.highlight?.content?.[0]
                          || (b.content ? b.content.slice(0,300)+'...' : '')
                      }} />
                  </Box>
                  <Box sx={{ mt:1 }}>
                    <Button component={Link} to={`/book/${b.id}`}>Read full →</Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {total > size && (
          <Box sx={{ display:'flex', justifyContent:'center', mt:2 }}>
            <Pagination
              count={Math.ceil(total/size)}
              page={page}
              onChange={(e,p)=>{ setPage(p); fetchData({ page:p }); }}
            />
          </Box>
        )}
      </Box>
    </Box>
  );
}

