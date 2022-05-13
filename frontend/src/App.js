import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios'
import moment from 'moment'
import sha256 from 'crypto-js/sha256';
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
import Base64  from 'base-64';

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
import SHA256 from "crypto-js/sha256";

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});


const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
    fontSize: 20,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 20,
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
  let genesisBlockTimeStamp = 1642287891509;
  let hosturl = "http://34.238.156.1:8093";

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
    axios.get(hosturl + '/transactions').then(response => {
      console.log("SUCCESS", response)
      const message = response.data.message
      console.log(message)
      let tmpList = []
      for (let i=0;i<message.length;i++){
        let txItem = message[i]
        const release_time  =  block_height_to_datetime(txItem.release_block_idx);
        const relation_time  =  block_height_to_datetime(txItem.relation_block_height);
        txItem.release_time = release_time;
        txItem.relation_time = relation_time;
        const hashDigest = sha256(txItem.decrypted_msg).toString();
        txItem.cipher_hash = hashDigest;
        console.log("~!!!!!!!!!!!!!!~~~~~~~~~~~~~~~~~~",txItem);
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

  function block_height_to_datetime(block_height){
    let timestamp = genesisBlockTimeStamp + 30000*block_height;
    const release_time  =  moment(timestamp).format('yy.MM.DD HH:mm')
    return release_time;
  }


  async function fetchLastTransactions(){
    if(currentBlockHeight !== -1){
      const response = await axios.get(hosturl + '/lastTransactions/' + currentBlockHeight);
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
    const response = await axios.get(hosturl + '/lastBlock');
    if(response.data.resultStatus === 'SUCCESS'){
      console.log("lastBlock SUCCESS");
      const block = response.data.message
      if (block.height !== undefined) {
        console.log("~~~~~~~~~~~~~~~~~~~~~~~~", block.height)
        console.log("~~~~~~~~~~~~~~~~~~~~~~~~~",Date.now());
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
                  <StyledTableCell>transaction id</StyledTableCell>
                  <StyledTableCell>publisher</StyledTableCell>
                  <StyledTableCell align="left">publish time</StyledTableCell>
                  <StyledTableCell>cipher</StyledTableCell>
                  <StyledTableCell align="left">release time</StyledTableCell>
                  <StyledTableCell align="left">released message</StyledTableCell>
                </TableRow>
              </TableHead>
              {
                getTransactionList && getTransactionList.length > 0
                    ? <TableBody>
                {getTransactionList.map((item) => (
                    <StyledTableRow key={item.tx_id}>
					  <StyledTableCell align="left">
					    {item.tx_id}
					  </StyledTableCell>
                      <StyledTableCell align="left">{item.from_address != undefined ? item.from_address.substring(0,30) + "..." : ""}</StyledTableCell>
                      <StyledTableCell align="left">{item.relation_time}</StyledTableCell>
                      <StyledTableCell align="left">{item.cipher_hash != undefined ? item.cipher_hash.substring(0,40) + "..." : ""}</StyledTableCell>
                      <StyledTableCell align="left">{item.release_time}</StyledTableCell>
					  <StyledTableCell align="left">{item.decrypted_msg}</StyledTableCell>
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
