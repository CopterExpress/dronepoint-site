import { Box, makeStyles, Typography } from '@material-ui/core'
import { Battery20, Battery30, Battery50, Battery60, Battery80, Battery90, BatteryAlert, BatteryFull, BatteryStd } from '@material-ui/icons';
import clsx from 'clsx';
import React, { useContext } from 'react'
import { StationContext } from '../contexts/StationProvider';

const useStyles = makeStyles(theme => ({
    root: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
    },
    box: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
    },
    text: {
        fontSize: 32,
        fontWeight: '400',
    },
    icon: {
        transform: 'scale(3)',
        marginRight: 20,
    },
}));

const getIcon = (battery) => {
    if (battery === null || battery === undefined) {
        return BatteryStd;
    }
    if (battery === 100) {
        return BatteryFull;
    } else if (battery > 90) {
        return Battery90;
    } else if (battery > 80) {
        return Battery80;
    } else if (battery > 60) {
        return Battery60;
    } else if (battery > 50) {
        return Battery50;
    } else if (battery > 30) {
        return Battery30;
    } else if (battery > 20) {
        return Battery20;
    } else {
        return BatteryAlert;
    }
}

const Battery = () => {
    const classes = useStyles();
    const { data, connection } = useContext(StationContext);
    const Icon = getIcon(data.battery);

    return (
        <Box className={classes.root}>
            <Box className={classes.box}>
                <Icon className={classes.icon} />
                <Typography variant="h2" className={classes.text}>
                    { !connection.drone && '-' }
                    { connection.drone && data.battery + '%' }
                </Typography>
            </Box>
        </Box>
    )
}

export default Battery
