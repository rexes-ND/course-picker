import styled from "styled-components";

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
const LogoutLink = styled.a`
    color: white;
    text-decoration: none;
    font-size: 16px;
    /* align-items: center; */
    padding-top: 10px;
`

const Header = (props) => {
    return (
        <HeaderContainer>
            AUTOMATIC COURSE PICKER
            {props.login?(<LogoutLink href="http://localhost:8001/api/v1/auth/logout?next=http://localhost:3000/login">Logout</LogoutLink>):<></>}
        </HeaderContainer>
    )
}

export default Header;