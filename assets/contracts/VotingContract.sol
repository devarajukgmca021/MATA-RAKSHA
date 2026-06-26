// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingContract {
    struct Candidate {
        uint id;
        string name;
        string party;
        uint voteCount;
    }
    
    struct Election {
        string name;
        string district;
        uint candidateCount;
        mapping(uint => Candidate) candidates;
        mapping(address => bool) hasVoted;
        mapping(address => bool) isRegistered;
        bool finalized;
    }
    
    address public admin;
    uint public electionCount;
    mapping(uint => Election) public elections;
    
    event VoteCast(uint electionId, address voter, uint candidateId);
    event ElectionCreated(uint electionId, string name, string district);
    event ElectionFinalized(uint electionId);
    event VoterRegistered(uint electionId, address voterAddress);
    
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }
    
    constructor() {
        admin = msg.sender;
        electionCount = 0;
    }
    
    function createElection(string memory _name, string memory _district) public onlyAdmin returns (uint) {
        electionCount++;
        Election storage newElection = elections[electionCount];
        newElection.name = _name;
        newElection.district = _district;
        newElection.candidateCount = 0;
        newElection.finalized = false;
        
        emit ElectionCreated(electionCount, _name, _district);
        return electionCount;
    }
    
    function registerVoter(uint _electionId, address _voterAddress) public onlyAdmin {
        require(_electionId > 0 && _electionId <= electionCount, "Invalid election ID");
        require(_voterAddress != address(0), "Invalid voter address");
        
        Election storage election = elections[_electionId];
        require(!election.finalized, "Election is finalized");
        require(!election.isRegistered[_voterAddress], "Voter already registered");
        
        election.isRegistered[_voterAddress] = true;
        emit VoterRegistered(_electionId, _voterAddress);
    }
    
    function addCandidate(uint _electionId, string memory _name, string memory _party) public onlyAdmin {
        require(_electionId > 0 && _electionId <= electionCount, "Invalid election ID");
        
        Election storage election = elections[_electionId];
        require(!election.finalized, "Election is finalized");
        
        election.candidateCount++;
        election.candidates[election.candidateCount] = Candidate(
            election.candidateCount,
            _name,
            _party,
            0
        );
    }
    
    function vote(uint _electionId, uint _candidateId) public {
        require(_electionId > 0 && _electionId <= electionCount, "Invalid election ID");
        
        Election storage election = elections[_electionId];
        require(election.isRegistered[msg.sender], "Voter not registered for this election");
        require(!election.hasVoted[msg.sender], "Voter has already voted");
        require(_candidateId > 0 && _candidateId <= election.candidateCount, "Invalid candidate ID");
        require(!election.finalized, "Election is finalized");
        
        election.hasVoted[msg.sender] = true;
        election.candidates[_candidateId].voteCount++;
        
        emit VoteCast(_electionId, msg.sender, _candidateId);
    }
    
    function getCandidate(uint _electionId, uint _candidateId) public view returns (uint, string memory, string memory, uint) {
        require(_electionId > 0 && _electionId <= electionCount, "Invalid election ID");
        
        Election storage election = elections[_electionId];
        require(_candidateId > 0 && _candidateId <= election.candidateCount, "Invalid candidate ID");
        
        Candidate memory candidate = election.candidates[_candidateId];
        return (candidate.id, candidate.name, candidate.party, candidate.voteCount);
    }
    
    function getCandidateCount(uint _electionId) public view returns (uint) {
        require(_electionId > 0 && _electionId <= electionCount, "Invalid election ID");
        return elections[_electionId].candidateCount;
    }
    
    function hasVoted(uint _electionId, address _voterAddress) public view returns (bool) {
        require(_electionId > 0 && _electionId <= electionCount, "Invalid election ID");
        return elections[_electionId].hasVoted[_voterAddress];
    }
    
    function isRegistered(uint _electionId, address _voterAddress) public view returns (bool) {
        require(_electionId > 0 && _electionId <= electionCount, "Invalid election ID");
        return elections[_electionId].isRegistered[_voterAddress];
    }
    
    function finalizeElection(uint _electionId) public onlyAdmin {
        require(_electionId > 0 && _electionId <= electionCount, "Invalid election ID");
        
        Election storage election = elections[_electionId];
        require(!election.finalized, "Election already finalized");
        
        election.finalized = true;
        emit ElectionFinalized(_electionId);
    }
    
    function getWinner(uint _electionId) public view returns (string memory, string memory, uint) {
        require(_electionId > 0 && _electionId <= electionCount, "Invalid election ID");
        
        Election storage election = elections[_electionId];
        require(election.finalized, "Election not finalized");
        
        uint winningVoteCount = 0;
        uint winningCandidateId = 0;
        
        for (uint i = 1; i <= election.candidateCount; i++) {
            if (election.candidates[i].voteCount > winningVoteCount) {
                winningVoteCount = election.candidates[i].voteCount;
                winningCandidateId = i;
            }
        }
        
        Candidate memory winner = election.candidates[winningCandidateId];
        return (winner.name, winner.party, winner.voteCount);
    }
}
