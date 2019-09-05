import React, { Component } from 'react';

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
          value: ' - name: Insert trololo\n   lineinfile: dest=/etc/trololo state=present regexp="{{ trololo }}" insertafter="trololo" line="trololo"\n   notify: restart trololo\n'
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }


  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();
    var data = "{ \"in\": \"" + this.state.value + "\"}" ;
    console.log('submit');
    console.log(data);
    fetch('http://localhost:5000/api/', {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then(res => res.json())
      .then(res => console.log(res));
}

 render() {
    return (
    <div className="App">
      <form onSubmit={this.handleSubmit} method="POST" action="http://localhost:5000/api"></form>
        <div className="row">
          <div className="col-md-5">
            <textarea className="form-control" value={this.state.value} onChange={this.handleChange} id="exampleFormControlTextarea1" rows="30"/>
          </div>
          <div className="col-md-2">
                <br/><br/><br/><br/><br/><br/>
                <input type="submit" value="Process" class="btn btn-pill btn-light btn-block btn-lg" />
          </div>
          <div className="col-md-5">
              <textarea className="form-control" id="exampleFormControlTextarea1" rows="30"/>
          </div>
        </div>

    </div>
    );
  }
}

export default App;
