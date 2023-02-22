import './App.css';
import React from "react";
import ReactDOM from "react-dom";
import UploadComponent from "./components/Upload/Upload";
import 'bootstrap/dist/css/bootstrap.css'
// import Download from './components/Download/Download';
//import CircularIndeterminate from './components/CircularProgress/CircularProgress'
//import { CircularProgress } from '@mui/material';

//import Button from 'react-bootstrap/Button';

class App extends React.Component
 {
  state = {
    upload: {
      pictures:[],
      maxFileSize: 5242880,
      imgExtension: [".jpg", ".png"],
      defaultImages: []
    }
  };

   handleChange = files => 
  {
    const { pictures } = this.state.upload;
    console.warn({ pictures, files });

    this.setState(
      {
        ...this.state,
        upload: {
          ...this.state.upload,
          pictures: [...pictures, ...files]
        }
      },
      () => {
        console.warn("It was added!");
      }
    );
  };



  render() {
    return (
      <div className="App">
        <br></br>
        <h1>Welcome !!</h1>
        <h2>Free Mezuza's Proofreading!!!</h2>
        
        <div className=' App-header'>
          <UploadComponent className='upload'
            {...this.state.upload}
            handleChange={this.handleChange}
          />
          </div>
        {/* <Download></Download> */}
        {/* <CircularIndeterminate></CircularIndeterminate> */}
      </div>
    );
  }
}
const rootElement = document.getElementById("root");
ReactDOM.render(<App />, rootElement);