// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract KinmenKaoliangRWA is ERC721, Ownable, ReentrancyGuard, Pausable {
    struct Barrel {
        uint16 productionYear;
        uint256 volumeLiters;
        string storageLocation;
        bool redeemed;
    }

    uint256 public nextTokenId = 1;
    mapping(uint256 => Barrel) private barrels;

    constructor(address initialOwner)
        ERC721("Kinmen Kaoliang RWA", "KKRWA")
        Ownable(initialOwner)
    {}

    function mintBarrel(
        address to,
        uint16 productionYear,
        uint256 volumeLiters,
        string calldata storageLocation
    ) external onlyOwner {
        require(volumeLiters > 0, "Invalid volume");

        uint256 tokenId = nextTokenId++;
        _safeMint(to, tokenId);

        barrels[tokenId] = Barrel(
            productionYear,
            volumeLiters,
            storageLocation,
            false
        );
    }

    function redeemBarrel(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender, "Not owner");
        require(!barrels[tokenId].redeemed, "Already redeemed");

        barrels[tokenId].redeemed = true;
        _burn(tokenId);
    }
}
