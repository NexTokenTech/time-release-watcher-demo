import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios'
import BlockListCell from './compnents/BlockListCell.js'
import { routes } from "./routes";
import TransactionList from "./compnents/TransactionList"

import { styled } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell, { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import {Button} from "@mui/material";

// import { Link, HashRouter as Router, LinkProps } from "react-router-dom";
// import {BrowserRouter as Router,
//   Switch,
//   Route,
//   Link} from "react-router-dom";

//button
import Dialog from '@mui/material/Dialog';
import ListItemText from '@mui/material/ListItemText';
import ListItem from '@mui/material/ListItem';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import CloseIcon from '@mui/icons-material/Close';
import Slide from '@mui/material/Slide';

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});


const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  '&:last-child td, &:last-child th': {
    border: 0,
  },
}));

const MyThemeComponent = styled(Button)(({ theme }) => ({
  margin:theme.spacing(5)
}));

function App() {
  const [getTransactionList, setGetTransactionList] = useState([])

  let currentBlockHeight = -1
  let currentTransactionHeight = -1

  useEffect(()=>{
    fetchTransactions()
  }, [])

  useEffect(()=>{
    const timer = setInterval(refreshPage, 4000);
  }, [])

  async function refreshPage(){
    console.log("i request")
    await fetchLastBlock()
  }


  function fetchTransactions() {
    axios.get('/api/transactions').then(response => {
      console.log("SUCCESS", response)
      const message = response.data.message
      console.log(message)
      let tmpList = []
      for (let i=0;i<message.length;i++){
        const txItem = message[i]
        if(txItem.decrypted_msg){
          tmpList.push(txItem)
        }
      }
      setGetTransactionList(tmpList)
    }).catch(error => {
      console.log("FAIL")
      console.log(error)
    })
  }


  async function fetchLastTransactions(){
    if(currentBlockHeight !== -1){
      const response = await axios.get('/api/lastTransactions/' + currentBlockHeight);
      if(response.data.resultStatus === 'SUCCESS'){
        console.log("lastTransactions SUCCESS");
        for(let i=0;i<response.data.message.length;i++){
          setGetTransactionList(prevState => [response.data.message[i],...prevState]);
          currentTransactionHeight = response.data.message[i].release_block_idx
        }
        setCurrentBlockHeight(response)
      }else{
        console.log("fetchLastTransactions FAIL")
      }
    }
  }

  async function fetchLastBlock() {
    const response = await axios.get('/api/lastBlock');
    if(response.data.resultStatus === 'SUCCESS'){
      console.log("lastBlock SUCCESS");
      const block = response.data.message
      if (block.height !== undefined) {
        console.log("~~~~~~~~~~~~~~~~~~~~~~~~", block.height)
        console.log("~~~~~~~~~~~~~~~~~~~~~~~~", currentTransactionHeight)
        if(block.height !== currentTransactionHeight){
          setCurrentBlockHeightByHeight(block.height)
          await fetchLastTransactions()
        }
      }
    }else{
      console.log("fetchLastBlock FAIL")
    }
  }

  function setCurrentBlockHeightByHeight(height){
    currentBlockHeight = height
  }

  function setCurrentBlockHeight(response){
    const blocks = response.data.message
      if(blocks.length > 0){
        const block = blocks[0]
        currentBlockHeight = block.height
      }
  }

  return (
      <div>
        <TableContainer component={Paper}>
            <Table sx={{ minWidth: 700 }} aria-label="customized table">
              <TableHead>
                <TableRow>
                  <StyledTableCell>tx_id</StyledTableCell>
                  <StyledTableCell>chiper</StyledTableCell>
                  <StyledTableCell align="left">decrypted_msg</StyledTableCell>
                  <StyledTableCell align="left">time_release_block_height</StyledTableCell>
                  <StyledTableCell align="left">block_height</StyledTableCell>
                </TableRow>
              </TableHead>
              {
                getTransactionList && getTransactionList.length > 0
                    ? <TableBody>
                {getTransactionList.map((item) => (
                    <StyledTableRow key={item.tx_id}>
					  <StyledTableCell component="th" scope="row">
					    {item.tx_id}
					  </StyledTableCell>
                      <StyledTableCell align="left">{item.chiper}</StyledTableCell>
					  <StyledTableCell align="left">{item.decrypted_msg}</StyledTableCell>
					  <StyledTableCell align="left">{item.release_block_idx}</StyledTableCell>
					  <StyledTableCell align="left">{item.relation_block_height}</StyledTableCell>
					</StyledTableRow>
              ))}
              </TableBody>
                    : <TableBody></TableBody>
              }
            </Table>
          </TableContainer>
      </div>
  );
}

export default App;
