import { Box, Divider, makeStyles, useMediaQuery } from '@material-ui/core'
import React, { useContext, useState } from 'react'
import { StationContext } from '../contexts/StationProvider';
import { getAllCells } from '../utils/cells';
import ActionBox from './ActionBox';
import DroneInfo from './DroneInfo';
import DroneMap from './DroneMap';
import Logger from './Logger';
import Logo from './Logo';
import SystemStatus from './SystemStatus';
import VideoBox from './VideoBox';

const useStyles = makeStyles(theme => ({
    root: {

    },
    main: {
        display: 'flex',
        alignItems: 'flex-start',
    },
    left: {
        flex: '33%',
    },
    middle: {
        flex: '34%',
        height: '806px',
        display: 'flex',
        flexDirection: 'column',
    },
    right: {
        flex: '33%',
    },
    mobileBox: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'stretch',
        height: 'max(100vh, 900px)',
    },
    mobileVideo: {
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'stretch',
        widthL: '100%',
        flex: 'auto',
    },
    mobileVideoItem: {
        flex: '50%',
    },
}));

const MainPage = () => {
    const classes = useStyles();
    const { data, startTest, video, connection } = useContext(StationContext);
    const [cell, setCell] = useState(0);
    const allCells = getAllCells();
    const isMobile = useMediaQuery(theme => theme.breakpoints.down('sm'))

    const handleTestStart = (password, testType) => {
        console.log(testType);
        startTest(allCells[cell], password, testType)
    }

    const handleCellChange = (e) => {
        setCell(e.target.value);
    }

    if (isMobile) return (
        <Box className={classes.mobileBox}>
            <Box>
                <DroneMap
                height={250}
                dronePos={data.pos}
                droneHistory={data.drone_history}
                stationPos={data.station_pos}
                isConnected={connection.drone}
                />
            </Box>
            <Divider />
            <Box>
                <SystemStatus />
                <Divider />
                <ActionBox
                allCells={allCells}
                cell={cell} 
                onCellChange={handleCellChange} 
                onTest={handleTestStart}
                />
            </Box>
            <Box className={classes.mobileVideo}>
                <VideoBox
                className={classes.mobileVideoItem}
                ws={true}
                src={'/'}
                type="station"
                />
                <Divider />
                <VideoBox
                className={classes.mobileVideoItem}
                ws={true}
                type="drone"
                src={'/'}
                />
            </Box>
        </Box>
    )

    return (
        <React.Fragment>
            <Box className={classes.main}>
                <Box className={classes.left}>
                    <DroneMap
                    height={400}
                    dronePos={data.pos}
                    droneHistory={data.drone_history}
                    stationPos={data.station_pos}
                    isConnected={connection.drone}
                    />
                    <Divider />
                    <DroneInfo height={360 + 16} />
                </Box>
                <Box className={classes.middle}>
                    <SystemStatus />
                    <Divider />
                    <ActionBox
                    allCells={allCells}
                    cell={cell} 
                    onCellChange={handleCellChange} 
                    onTest={handleTestStart}
                    />
                    <Logger />
                </Box>
                <Box className={classes.right}>
                    <VideoBox
                    active={true}
                    ws={true}
                    src={'/'}
                    height={400}
                    type="station"
                    />
                    <Divider />
                    <VideoBox
                    active={true}
                    ws={true}
                    type="drone"
                    src={'/'}
                    height={400}

                    />
                </Box>
            </Box>
        </React.Fragment>
    )
}

export default MainPage
