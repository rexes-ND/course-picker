import styled from "styled-components";
import {Link} from "react-router-dom";

const HeaderContainer = styled.div`
    display: flex;
    font-size: 32px;
    color: white;
    height: 64px;
    padding-left: 20px;
    padding-right: 20px;
    padding-top: 16px;
    /* border-bottom: 1px solid #cdcdcd; */
    background-color: #2c3e50;
    justify-content: space-between;
`
const LinkContainer = styled.div`
    
    font-size: 16px;
    /* align-items: center; */
    padding-top: 10px;
`
// const ProfileLink = styled.a`
//     color: white;
//     text-decoration: none;
//     margin-right: 15px;
// `

const LogoutLink = styled.a`
    color: white;
    text-decoration: none;
`

const Header = (props) => {
    return (
        <HeaderContainer>
            <Link to="/" style={{"color": "white", "textDecoration": "none"}}>AUTOMATIC COURSE PICKER</Link>
            {props.login?(
                <LinkContainer>
                    {/* <ProfileLink href={"http://localhost:3000/user"}>
                        {props.user.firstName}
                    </ProfileLink> */}
                    <Link to='/user' style={{"color": "white", "textDecoration": "none", "marginRight": "15px"}}>{props.user.firstName}</Link>
                    <LogoutLink href="http://localhost:8001/api/v1/auth/logout?next=http://localhost:3000/login">
                        Logout
                    </LogoutLink>
                </LinkContainer>):<></>}
        </HeaderContainer>
    )
}

export default Header;