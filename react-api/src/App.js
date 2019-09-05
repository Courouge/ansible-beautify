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
    var payload = {
        a: 1,
        b: 2
    };
    var data = new FormData();
    data.append( "json", JSON.stringify( payload ) );

    fetch('http://localhost:5000/api', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        },
      body: data
    })
  }

 render() {
    return (
    <div className="App">
      <form onSubmit={this.handleSubmit} method="POST" action="http://localhost:5000/api">
        <div className="row">
          <div className="col-md-5">
            <textarea className="form-control" value={this.state.value} onChange={this.handleChange} id="exampleFormControlTextarea1" rows="15"/>
          </div>

          <div className="col-md-2">
            <span className="align-middle">
                <input type="submit" value="Envoyer" />
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
