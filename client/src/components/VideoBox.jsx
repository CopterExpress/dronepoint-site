import { Box, makeStyles, Typography } from '@material-ui/core'
import React, { useContext, useEffect, useRef, useState } from 'react'
import NotAvailable from './NotAvailable';
import JSMpeg from '@cycjimmy/jsmpeg-player';
import { DP_VIDEO_URL, sendGetVideoEvent, subscribeVideoEvent, unsubscribeVideoEvent } from '../socket';
import io from 'socket.io-client';
import 'dotenv/config';
import clsx from 'clsx';

const useStyles = makeStyles(theme => ({
    root: {
        height: props => props.height,
        backgroundColor: '#F0F0F0',
    },
    image: {
        height: '100%',
        width: '100%',
    }
}));

const VideoBox = ({ height, src, ws, type, className }) => {
    const classes = useStyles({ height });
    const imageRef = useRef();
    const [isValidSrc, setIsValidSrc] = useState(true);

    useEffect(() => {
        if (ws) {
            const socket = io(process.env.REACT_APP_VIDEO_URL);
            socket.on(type === 'drone' ? 'dronedata' : 'stationdata', data => {
                imageRef.current.src = 'data:image/jpeg;base64,' + data;
            })
            socket.on('connect', e => {
                console.log('Connect');
            })
        }
    }, []);

    const handleError = () => setIsValidSrc(false);

    if (!isValidSrc) return (
        <Box className={clsx(classes.root, className)}>
            <NotAvailable />
        </Box>
    )
    
    return (
        <Box className={clsx(classes.root, className)}>
            {!ws && <img className={classes.image} ref={imageRef} src={src} onError={handleError}/>}
            {/* {ws && <canvas className={classes.image} ref={imageRef} onError={handleError}/>} */}
            {ws && <img className={classes.image} ref={imageRef} src={src} />}
        </Box>
    )
}

export default VideoBox
