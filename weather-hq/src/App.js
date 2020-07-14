import React, { Component } from 'react'
import './App.css'

const Minio = require('minio')

class App extends Component {
  constructor () {
    super()
    this.state = {
      mc: undefined,
      records: {},
      loop: false,
      sampleTime: 15000
    }
  }

  getImageUrl (record) {
    const { path } = this.getRecordInfo(record)
    return `http://**REMOVED**/${path}`
  }

  getRecordInfo (record) {
    const path = unescape(record.s3.object.key)
    const deviceName = path.split('/')[0]
    return {
      path,
      deviceName
    }
  }

  componentWillMount () {
    const mc = new Minio.Client({
      endPoint: '**REMOVED**',
      port: 9000,
      useSSL: false,
      accessKey: '**REMOVED**',
      secretKey: '**REMOVED**'
    })

    const poller = mc.listenBucketNotification('**REMOVED**', '', '', ['s3:ObjectCreated:*'])
    poller.on('notification', record => {
      const { deviceName } = this.getRecordInfo(record)
      this.setState({
        records: {
          ...this.state.records,
          [deviceName]: record
        }
      })
      // console.log(path, deviceName)
      console.log(record)
      // // console.log('New object: %s/%s (size: %d)', record.s3.bucket.name, record.s3.object.key, record.s3.object.size)
    })
    this.setState({ mc })
  }

  formatDate (dateString) {
    const date = new Date(dateString)
    const options = { weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' }
    return date.toLocaleDateString('sv-SE', options)
  }

  render () {
    const devices = Object.keys(this.state.records).sort()
    return (
      <div className='app'>
        {devices.map((deviceName) => {
          const record = this.state.records[deviceName]
          const imageSrc = this.getImageUrl(record)
          return (
            <div
              key={imageSrc} className='device-photo' style={{
                backgroundImage: `url('${imageSrc}')`
              }}
            >
              <div className='title-wrapper'>
                <p className='title'>{deviceName}</p>
                <p className='timestamp'>{this.formatDate(record.eventTime)}</p>
              </div>
            </div>
          )
        })}
      </div>
    )
  }
}

export default App
