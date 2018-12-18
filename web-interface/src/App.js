import React, { Component } from 'react';
import './App.css';

const Minio = require('minio')

class App extends Component {
  constructor() {
    super()
    this.state = {
      mc: undefined,
      latestImage: {},
      loop: false,
      sampleTime: 15000
    }
  }
  componentWillMount() {
    const mc = new Minio.Client({
      endPoint: '***REMOVED***',
      port: 9000,
      useSSL: false,
      accessKey: '***REMOVED***',
      secretKey: '***REMOVED***'
    })
    this.setState({ mc }, this.fetchLatestImages)
    // const stream = mc.listObjects('***REMOVED***','', true)
    // stream.on('data', this.handleData.bind(this))
    // stream.on('error', this.handleError.bind(this))
    // var listener = mc.listenBucketNotification('***REMOVED***', '/***REMOVED***/2018/12/18/', '.jpg', ['s3:ObjectCreated:*'])
    // listener.on('notification', this.handleData.bind(this))
  }
  fetchLatestImages(device, date) {
    const bucketName = '***REMOVED***'
    const devices = device ? [device] : ['***REMOVED***', '***REMOVED***', '***REMOVED***']
    const currentDate = !date 
      ? this.convertDateToUTC(new Date()) 
      : new Date(date)
    const { mc, sampleTime, loop } = this.state
    devices.forEach((deviceName) => {
      let prefix = `${deviceName}/${currentDate.getFullYear()}/${currentDate.getMonth() + 1}/${currentDate.getDate()}/`
      prefix = date ?  prefix + `${currentDate.getHours()}${currentDate.getMinutes()}` : prefix
      const stream = mc.listObjects(bucketName, prefix, false)
      stream.on('data', (obj) => {
        this.handleData(deviceName, obj)
      })
      stream.on('error', this.handleError.bind(this))
      if (!loop) { // warm up
        setTimeout(() => {
          this.setState({
            loop: true,
          })
        }, sampleTime)
      }
    })
  }
  handleData(deviceName, obj) {
    const { latestImage } = this.state
    const { name, lastModified } = obj
    if (!latestImage[deviceName]) {
      latestImage[deviceName] = obj
    }
    const currentImage = latestImage[deviceName]
    if (currentImage.lastModified < lastModified) {
      latestImage[deviceName] = obj
    }
    this.setState({ latestImage })

    setTimeout(() => {
      this.fetchLatestImages(deviceName, latestImage.lastModified)
    }, 15000)
  }
  handleError = console.error
  convertDateToUTC(date) {
    return new Date(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate(), date.getUTCHours(), date.getUTCMinutes(), date.getUTCSeconds()); 
  }
  render() {
    const devices = Object.keys(this.state.latestImage)
    return (
      <div className="App">
        { devices.map((deviceName) => {

          return <p>{`hello`}</p>
        })}
      </div>
    );
  }
}

export default App;
