import React, { Component } from 'react';

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
          value: '- name: Insert trololo\n  lineinfile: dest=/etc/trololo state=present regexp="{{ trololo }}" insertafter="trololo" line="trololo"\n  notify: restart trololo\n',
          res: ''
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }


  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();
    fetch(process.env.REACT_APP_API, {
      method: 'POST',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({ in: this.state.value }),
    })
      .then(res => { return res.json() })
      .then(json => this.setState({res: json}))
}

 render() {
    return (
    <div className="App">
      <form onSubmit={this.handleSubmit} method="POST">
        <div className="row">
          <div className="col-md-5">
            <textarea className="form-control" value={this.state.value} onChange={this.handleChange} id="exampleFormControlTextarea1" rows="16"/>
          </div>
          <div className="col-md-2">
                <br/><br/><br/><br/><br/><br/>
                <input type="submit" value="Process" class="btn btn-pill btn-light btn-block btn-lg" />
          </div>
          <div className="col-md-5">
              <textarea className="form-control text-muted" value={this.state.res.out} id="exampleFormControlTextarea1" rows="16"/>
          </div>
        </div>
      </form>
    </div>
    );
  }
}

export default App;
