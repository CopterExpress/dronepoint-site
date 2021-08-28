import { Box, Grid, makeStyles, Typography } from '@material-ui/core'
import { Check, Close } from '@material-ui/icons';
import React, { useContext } from 'react'
import { StationContext } from '../contexts/StationProvider';

const useStyles = makeStyles(theme => ({
    root: {
        marginBottom: 20,
        marginTop: 20,
    },
    icon: {
        fontSize: 50,
        marginTop: 10,
        marginBottom: 10,
        [theme.breakpoints.down('sm')]: {
            fontSize: 30,
            marginTop: 5,
            marginBottom: 5,
        }
    },
    statusBox: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
}));

const SystemStatus = () => {
    const classes = useStyles();
    const { connection: { drone, station } } = useContext(StationContext);

    const getStatusIcon = (val) => val ? 
    <Check className={classes.icon} color="secondary"/> : 
    <Close className={classes.icon} color="error" />

    const getStatusText = (val) => val ? 'Connected' : 'Disconnected'

    return (
        <Grid container className={classes.root} justify="space-evenly">
            <Grid item className={classes.statusBox}>
                <Typography variant="h2" className={classes.text}>Drone</Typography>
                {getStatusIcon(drone)}
                <Typography variant="h3">{getStatusText(drone)}</Typography>
            </Grid>
            <Grid item className={classes.statusBox}>
                <Typography variant="h2" className={classes.text}>Station</Typography>
                {getStatusIcon(station)}
                <Typography variant="h3">{getStatusText(station)}</Typography>
            </Grid>
        </Grid>
    )
}

export default SystemStatus
