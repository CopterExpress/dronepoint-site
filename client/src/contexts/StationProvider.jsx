import React, { createContext, useEffect, useRef, useState } from 'react'
import { toast } from 'react-toastify';
import { login, sendGetDataEvent, sendGetVideoEvent, sendLogEvent, sendTestEvent, subscribeConnectEvent, 
    subscribeDataEvent, subscribeErrorEvent, subscribeLogEvent, subscribeVideoEvent, unsubscribeVideoEvent } from '../socket';

export const StationContext = createContext({
    data: {},
    loading: true,
    startTest: (cell, password) => {},
    authenticate: async (password) => false,
    isAuthenticated: false,
    connection: { drone: false, station: false },
    video: { drone: null, station: null },      
    isConnected: false,
    logInfo: [],
})

const StationProvider = ({ children, timeout=500 }) => {
    const [data, setData] = useState(null);
    const [droneConnected, setDroneConnected] = useState(false);
    const [stationConnected, setStationConnected] = useState(false);
    const [loading, setLoading] = useState(true);
    const [stFrame, setStFrame] = useState(null);
    const [droneFrame, setDroneFrame] = useState(null);
    const [logInfo, setLogInfo] = useState([]);

    const handleConnectEvent = () => {
        console.log('Connected');
        setLoading(false);
    }

    const handleDataEvent = (data) => {
        if (!data || !data.connection) return
        setDroneConnected(data.connection.drone);
        setStationConnected(data.connection.station);
        delete data.connection;
        setData(data);
    }

    const handleLogEvent = (data) => {
        setLogInfo(data);
    }

    const handleErrorEvent = (err) => {
        console.log(err);
        toast.error(err);
    }
    
    useEffect(() => {
        subscribeDataEvent(handleDataEvent);
        subscribeConnectEvent(handleConnectEvent);
        subscribeErrorEvent(handleErrorEvent);
        subscribeLogEvent(handleLogEvent);

        let check = true;
        const handleVideoEvent = (data) => {
            setStFrame(URL.createObjectURL(
                new Blob([data.station], { type: 'image/jpeg' })
            ))
            setDroneFrame(URL.createObjectURL(
                new Blob([data.drone], { type: 'image/jpeg' })
            ))
            check = true
        }

        subscribeVideoEvent(handleVideoEvent);
        
        const interval = setInterval(() => {
            if (check) {
                sendGetVideoEvent();
                check = false;
            }
        }, 20);

        const dataInterval = setInterval(() => {
            sendGetDataEvent();
        }, timeout);

        const logInterval = setInterval(() => {
            sendLogEvent();
        }, timeout);

        return () => {
            clearInterval(interval);
            clearInterval(dataInterval);
            clearInterval(logInterval);
            unsubscribeVideoEvent();
        }
    }, []);

    return (
        <StationContext.Provider value={{
            data: data,
            loading: loading,
            startTest: (cell, password, testType) => sendTestEvent(cell, password, testType),
            connection: { drone: droneConnected, station: stationConnected },
            isConnected: stationConnected && droneConnected,
            video: { drone: droneFrame, staion: stFrame },
            logInfo: logInfo,
        }}>
            {children}
        </StationContext.Provider>
    )
}

export default StationProvider
