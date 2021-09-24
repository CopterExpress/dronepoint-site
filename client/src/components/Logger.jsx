import { Box, makeStyles } from '@material-ui/core'
import clsx from 'clsx';
import React from 'react'
import { useRef } from 'react';
import { useContext } from 'react';
import { useEffect } from 'react';
import { StationContext } from '../contexts/StationProvider';
import { sendLogEvent, subscribeLogEvent, unsubscribeLogEvent } from '../socket';

const useStyles = makeStyles(theme => ({
    root: {
        padding: '10px 15px',
        fontFamily: 'Courier, sans-serif',
        fontSize: 12,
        lineHeight: 1.3,
        color: '#fff',
        backgroundColor: '#2c3e50',
        '-webkit-border-radius': '0px 0px 6px 6px',
        '-moz-border-radius': '0px 0px 6px 6px',
        borderRadius: '0px 0px 6px 6px',
        marginLeft: 15,
        marginRight: 15,
        height: '100%',
        overflowY: 'scroll',
        maxWidth: '33vw',
    },
    code: {
        maxWidth: 'inherit',
    },
    header: {
        marginTop: 10,
        padding: '5px 5px 5px 10px',
        fontFamily: 'Roboto, sans-serif',
        fontSize: 18,
        color: '#fff',
        borderRadius: '6px 6px 0px 0px',
        '-webkit-border-radius': '6px 6px 0px 0px',
        '-moz-border-radius': '6px 6px 0px 0px',
        userSelect: 'none',
        backgroundColor: '#0074D9',
        marginLeft: 15,
        marginRight: 15,

    },
}));

const Logger = () => {
    const classes = useStyles();
    const { logInfo } = useContext(StationContext);
    const boxRef = useRef();
    
    useEffect(() => {
        boxRef.current.scrollTo(0, boxRef.current.scrollHeight);
    }, [logInfo.length]);

    return (
        <React.Fragment>
            <Box className={classes.header}>
                INFO
            </Box>
            <div className={clsx(classes.root, 'custom-scrollbar')} ref={boxRef}>
                <pre>
                    <code className={classes.code}>
                        {logInfo.map(message => (
                            <React.Fragment>
                                {message}{'\n'}
                            </React.Fragment>
                        ))}
                    </code>
                </pre>
            </div>
        </React.Fragment>
    )
}

export default Logger
