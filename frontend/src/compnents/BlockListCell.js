import "./BlockListCell.scss"
import React from "react"
import axios from "axios"

function BlockListCell(props){
	console.log(props);
	function transactionBtnPressed() {
		console.log("transactionBtnPressed");
	}
	return (
		<div className={"blocklistcell"}>
			<div className="row1">
				<div className="column1">{props.blockid}</div>
				<div className="column2">hash: {props.hash}</div>
				<div className="column3">prevHash: {props.prevhash}</div>
				<div className="column4">publicKey: {props.publickey}</div>
				<div className="column5">solution: {props.solution}</div>
			</div>
			<button className={"transaction"} onClick={() => {
                props.getTransactions(props)
                // 传递的值在props里面，直接拿来调用，使用箭头函数是为了让this可以正常在函数里使用
            }}>transactions</button>
		</div>
	);
}
export default BlockListCell;