import { Box, makeStyles } from '@material-ui/core'
import React from 'react'

const useStyles = makeStyles(theme => ({
    root: {
        display: 'flex',
        justifyContent: 'center',
    },
    image: {
        height: '300px',
    },
}));

const Logo = () => {
    const classes = useStyles();
    return (
        <Box className={classes.root}>
            <img 
            src="https://static.tildacdn.com/tild3138-6633-4162-b562-353339303438/photo.png"
            className={classes.image}
            />
        </Box>
    )
}

export default Logo
