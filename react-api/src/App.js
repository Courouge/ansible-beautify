import React, { Component } from 'react';

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            Data: [{
                "datainput": "yoloin",
                "dataoutput": "yoloout"
            }]
        }
         this.handleSubmit = this.handleSubmit.bind(this);
    }

 handleSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const data = new FormData(form);
    console.log(form)

    fetch('/', {
      method: 'POST',
      body: data,
    });
  }

 render() {
    return (
    <div className="App">
      <form onSubmit={this.handleSubmit} method="post" action="/">
        <div className="row">
          <div className="col-md-5">
            <textarea className="form-control" id="exampleFormControlTextarea1" rows="15"/>
          </div>

          <div className="col-md-2">
            <span className="align-middle">
                <button>Send data!</button>
            </span>
          </div>

          <div className="col-md-5">
              <textarea className="form-control" id="exampleFormControlTextarea1" rows="15"/>
          </div>
        </div>
      </form>
    </div>
    );
  }
}

export default App;
