import React from 'react';
import './App.css';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container'
import Col from 'react-bootstrap/Col'
import Spinner from 'react-bootstrap/Spinner'
import 'bootstrap/dist/css/bootstrap.css';
import { Doughnut } from 'react-chartjs-2';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { youtubeid: '', answer: '', loading: false };
    this.colors = ["#FF3333", "#FF9C33", "#FFFE33", "#7BFF33", "#33FFEB", "#3388FF", "#8733FF", "#EA33FF", "#FF33A2", "#EACBFC", "#CBE8FC", "#CBFCD2", "#FBFCCB"]
  }


  handleSubmit = async (event) => {
    event.preventDefault();
    this.setState({ loading: true })
    console.log('submitted')
    try {
      let response = await fetch(`http://localhost:5000/?youtubeid=${this.state.youtubeid}`)
      let json = await response.json()
      console.log(json)
      this.setState({ loading: false })
      this.setState({ answer: json })
    } catch (error) {
      console.log(error)
      this.setState({ loading: false })
      this.setState({ answer: "error" })
    }
  }

  handleChange = (event) => {
    this.setState({ youtubeid: event.target.value });
  }

  renderAnswer = () => {
    if (this.state.answer == "error") {
      return (<span>An error occurred ensure that you key in the right id.</span>)
    } else if (this.state.answer != "") {
      let emotionData = []
      let emotionLabels = []
      
      for(let [key,value] of Object.entries(this.state.answer.emotion)){
        emotionData.push(value)
        emotionLabels.push(key)
      }
      let emotionColors = this.colors.slice(0,emotionLabels.length)

      let sentimentData = []
      let sentimentLabels = []
      
      for(let [key,value] of Object.entries(this.state.answer.sentiment)){
        sentimentData.push(value)
        sentimentLabels.push(key)
      }
      let sentimentColors = this.colors.slice(0,sentimentLabels.length)
      console.log("reached")
      console.log(emotionData)
      console.log(emotionLabels)
      console.log(emotionColors)
      
      return (
        <div style={{textAlign:"center"}}>
          <h2>Emotion Analysis</h2>
          <Doughnut data={{
            datasets: [{
              data: emotionData,
              backgroundColor: emotionColors
            }], labels: emotionLabels
          }} />
           <h2>Sentiment Analysis</h2>
          <Doughnut data={{
            datasets: [{
              data:sentimentData,
              backgroundColor:sentimentColors
            }], labels:sentimentLabels
          }} />
        </div>
      )
    } else {
      return undefined
    }
  }

  render = () => {
    return (
      <Container className="App" style={{ display: "flex", justifyContent: "center" }}>
        <Col md={8} lg={8}>
          <h1 style={{ marginBottom: "1em", marginTop: "0.3em" }}>Youtube Comments Sentiment Emotion</h1>
          <Form onSubmit={this.handleSubmit} className="form">
            <Form.Group>
              <Form.Control onChange={this.handleChange} type="search" placeholder="Key in youtube id here" />
            </Form.Group>
            <Button type="submit" style={{ marginBottom: "1em" }} variant="primary" type="submit">
              {this.state.loading ? <div><span>Scraping and inferencing ... </span> <Spinner
                as="span"
                animation="border"
                size="sm"
                role="status"
                aria-hidden="true"
              /></div> : <span>Submit</span>}
            </Button>
          </Form>
          <div style={{ textAlign: "justify",marginTop:"3em" }}>
            {this.state.loading ? undefined : this.renderAnswer()}
          </div>
        </Col>
      </Container>
    )
  }
}

export default App;