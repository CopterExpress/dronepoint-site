import { Box, makeStyles, MenuItem, Select, Typography } from '@material-ui/core'
import React from 'react'

const useStyles = makeStyles(theme => ({
    text: {
        fontSize: 28,
        [theme.breakpoints.down('sm')]: {
            fontSize: 18,
        },
    },
}));

const Cells = ({ value, onChange, allCells, className, disabled }) => {
    const classes = useStyles();
    return (
        <Select placeholder="Cell" onChange={onChange} value={value} className={className}
        disabled={disabled}>
            {allCells.map((cell, i) => (
                <MenuItem value={i}>
                    <Typography align="center" className={classes.text}>
                        (    x = {cell[0]}    y = {cell[1]}    z = {cell[2]})
                    </Typography>
                </MenuItem>
            ))}
        </Select>
    )
}

export default Cells
