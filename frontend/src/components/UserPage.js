import Header from './Header'
import styled from 'styled-components'
import { useState } from 'react'
import instance from '../Client'
import {
    Select,
    FormControl,
    InputLabel,
    MenuItem,
    Button,
    Modal,
    Box,
    Typography
} from '@mui/material'

const UserPageHeader = styled.div`
    font-size: 50px;
    margin-top: 50px;
    margin-bottom: 50px;
    text-align: center;
`

const UserPageBody = styled.div`
    width: 320px;
    margin: 0 auto;
    color: #2c3e50;
    font-size: 20px;
    text-align: center;
`

const UserPageLine = styled.div`
    margin-bottom: 10px;
`


const UserPage = (props) => {
    console.log(props.user)
    const [open, setOpen] = useState(false)
    const [msg, setMsg] = useState("")
    const [majorObj, setMajorObj] = useState({
        majorType: props.user.majorType,
        major: props.user.major,
        minor: props.user.minor
    })
    const majorTypeChange = (e) => {
        // props.setUser({
        //     ...props.user,
        //     majorType: e.target.value
        // })
        setMajorObj(prevMajorObj => {
            return {
                ...prevMajorObj,
                majorType: e.target.value
            }
        })
    }
    const majorChange = (e) => {
        // props.setUser({
        //     ...props.user,
        //     major: e.target.value
        // })
        if (e.target.value === majorObj['minor']){
            setMsg("We don't support that combination.")
            setOpen(true)
            return
        }
        setMajorObj(prevMajorObj => {
            return {
                ...prevMajorObj,
                major: e.target.value
            }
        })
    }
    const minorChange = (e) => {
        // props.setUser({
        //     ...props.user,
        //     minor: e.target.value
        // })
        if (e.target.value === majorObj['major']){
            setMsg("We don't support that combination")
            setOpen(true)
            return
        }
        setMajorObj(prevMajorObj => {
            return {
                ...prevMajorObj,
                minor: e.target.value
            }
        })
    }
    const handleClick = (e) => {
        console.log("Button Clicked")
        instance.post("http://localhost:8001/api/v1/user/update", majorObj)
        .then(res => {
            if (res.data['status'] === 200) {
                setMsg("Succesfully updated your information!")
                setOpen(true);
                props.setUser(prevUser => {
                    return {
                        ...prevUser,
                        majorType: majorObj.majorType,
                        major: majorObj.major,
                        minor: majorObj.minor
                    }
                })
            } else {
                setMsg("Something went wrong! Please try again.");
                setOpen(true);
                setMajorObj({
                    majorType: props.user.majorType,
                    major: props.user.major,
                    minor: props.user.minor
                })
            }
        }).catch(error => {
            console.log(error)
        })
    }
    console.log(majorObj)
    return (
        <>
            <Header login={props.login} user={props.user}/>
            <UserPageHeader>
                User Information
            </UserPageHeader>
            
            <UserPageBody>
                {(props.user["majorType"]==="" || props.user["major"]==="" || props.user["minor"]==="")?<UserPageLine
                    style={{
                        "color": "red"
                    }}
                >
                    <b>To use our service, please choose appropriate major or minor.</b>
                </UserPageLine>:<></>}
                <UserPageLine
                    style={{
                        "marginTop": "20px"
                    }}
                >
                    Name: {props.user.firstName}{" "}{props.user.lastName}
                </UserPageLine>
                <UserPageLine>
                    Student ID: {props.user.studentID}
                </UserPageLine>
                <UserPageLine>
                    <FormControl style={{"width": "150px"}}>
                        <InputLabel id="majortype-select-label">Major Type</InputLabel>
                        <Select
                            labelId="majortype-select-label"
                            value={majorObj.majorType}
                            onChange={majorTypeChange}
                        >
                            <MenuItem value="" divider>None</MenuItem>
                            <MenuItem value={true} divider>Double Major</MenuItem>
                            <MenuItem value={false}>Major/Minor</MenuItem>
                        </Select>
                    </FormControl>
                </UserPageLine>
                <UserPageLine>
                    <FormControl style={{"width": "150px"}}>
                        <InputLabel id="major-select-label">Major</InputLabel>
                        <Select
                            labelId="major-select-label"
                            value={majorObj.major}
                            onChange={majorChange}
                        >
                            <MenuItem value="" divider>None</MenuItem>
                            <MenuItem value="CS" divider>CS</MenuItem>
                            <MenuItem value="MAS">MAS</MenuItem>
                        </Select>
                    </FormControl>
                </UserPageLine>
                <UserPageLine>
                    <FormControl style={{"width": "150px"}}>
                        {(majorObj.majorType === true)?
                        <InputLabel id="minor-select-label">
                            Second Major
                        </InputLabel>:
                        <InputLabel id="minor-select-label">
                            Minor
                        </InputLabel>}
                        <Select
                            labelId="minor-select-label"
                            value={majorObj.minor}
                            onChange={minorChange}
                        >
                            <MenuItem value="" divider>None</MenuItem>
                            <MenuItem value="CS" divider>CS</MenuItem>
                            <MenuItem value="MAS">MAS</MenuItem>
                        </Select>
                    </FormControl>
                </UserPageLine>
                <Button
                    variant="outlined"
                    style={{
                        "marginTop": "20px"
                    }}
                    onClick={handleClick}
                >
                    Update User Information
                </Button>
                <Modal
                    open={open}
                    onClose={()=>{setOpen(false)}}
                    aria-labelledby="modal-modal-title"
                    aria-describedby="modal-modal-description"
                >
                    <Box
                        sx={{
                            position: 'absolute',
                            top: '50%',
                            left: '50%',
                            transform: 'translate(-50%, -50%)',
                            width: 400,
                            bgcolor: 'background.paper',
                            border: '2px solid #000',
                            boxShadow: 24,
                            p: 4,
                        }}
                    >
                        <Typography id="modal-modal-title" variant="h6" component="h2">
                            {/* Your information is successfully updated! */}
                            {msg}
                        </Typography>
                        {/* <Typography id="modal-modal-description">
                            Hello, Erkhes!
                        </Typography> */}
                    </Box>
                </Modal>
            </UserPageBody>
        </>
    )
}

export default UserPage