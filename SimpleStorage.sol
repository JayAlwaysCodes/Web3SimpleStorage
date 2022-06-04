//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    //this will get initialize to zero
    uint256 favoriteNumber;

    struct People {
        uint256 favoriteNumber;
        string name;
    }
    People[] public people;
    mapping(string => uint256) public nameTofavoriteNumber;

    //address favoriteAddress = 0xa3Cb51f20A4259feCB87c03F36763b2EDa56837f;
    function store(uint256 _favoriteNumber) public returns (uint256) {
        favoriteNumber = _favoriteNumber;
        return _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameTofavoriteNumber[_name] = _favoriteNumber;
    }
}
