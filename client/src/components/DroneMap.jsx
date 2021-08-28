import { Box, makeStyles, Typography } from '@material-ui/core'
import { Map, Placemark, Polyline } from 'react-yandex-maps';
import React, { useCallback, useContext, useMemo } from 'react'

const useStyles = makeStyles(theme => ({
    root: {
        height: props => props.height,
    },
}));

const droneSize = 80;

const DroneMap = ({ height, isConnected, dronePos, stationPos, droneHistory }) => {
    const classes = useStyles({ height });

    if (!isConnected) {
        return (
            <Box className={classes.root}>
                <Typography align="center" variant="h2">
                    No Drone Connected
                </Typography>
            </Box>
        )
    }
    
    return (
        <Box className={classes.root}>
            <Map defaultState={{ center: dronePos, zoom: 19 }} width={'100%'} height={'100%'}>
                <Placemark geometry={dronePos} options={{
                    iconLayout: 'default#image',
                    iconImageHref: '/drone.png',
                    iconImageSize: [droneSize, droneSize],
                    iconImageOffset: [-droneSize / 2, -droneSize / 2],
                    iconShape: {
                        type: 'Circle',
                        coordinates: [0, 0],
                        radius: 20
                    },
                }}/>
                <Placemark geometry={stationPos} />
                <Polyline 
                geometry={droneHistory}
                options={{
                    strokeColor: '#F24949',
                    strokeWidth: 4,
                    strokeOpacity: 0.8,
                }}
                />
            </Map>
        </Box>
    )
}

export default React.memo(DroneMap)
