import { Button, Dialog, DialogActions, DialogContent, DialogTitle, makeStyles, TextField, Typography } from '@material-ui/core'
import React, { useState } from 'react'

const useStyles = makeStyles(theme => ({
    root: {
        minWidth: 400,
        minHeight: 200,
    },
    closeBtn: {
        color: 'white',
        backgroundColor: theme.palette.error.main,
        '&:hover': {
            backgroundColor: theme.palette.error.dark,
        }
    }
}));

const LoginDialog = ({ onClose, open, onSubmit }) => {
    const classes = useStyles();
    const [password, setPassword] = useState('');

    const handleSubmit = () => {
        onSubmit(password);
    }

    return (
        <Dialog onClose={onClose} open={open}
        PaperProps={{ className: classes.root }}>
            <DialogTitle>
                <Typography variant="h2">Enter Password</Typography>
            </DialogTitle>
            <DialogContent>
                <TextField 
                fullWidth
                value={password} 
                type="password"
                label="Password"
                onChange={(e) => setPassword(e.target.value)} />
            </DialogContent>
            <DialogActions >
                <Button 
                variant="contained" 
                onClick={handleSubmit} 
                color="secondary">
                    Start Test
                </Button>
                <Button 
                variant="contained"
                onClick={onClose} 
                className={classes.closeBtn}>
                    Close
                </Button>
            </DialogActions>
        </Dialog>

    )
}

export default LoginDialog
