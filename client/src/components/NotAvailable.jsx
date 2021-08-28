import { Box, makeStyles, Typography } from '@material-ui/core'
import SentimentVeryDissatisfiedIcon from '@material-ui/icons/SentimentVeryDissatisfied';
import React from 'react'

const useStyles = makeStyles(theme => ({
    root: {
        width: '100%',
        height: '100%',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
    },
    icon: {
        fontSize: 60,
    },
    text: {
        fontSize: 24,
    },
}));

const NotAvailable = () => {
    const classes = useStyles();
    return (
        <Box className={classes.root}>
            <SentimentVeryDissatisfiedIcon className={classes.icon} />
            <Typography variant="h2" className={classes.text}>Not available</Typography>
        </Box>
    )
}

export default NotAvailable
