import random

class Match:
    def __init__(self, id, players):
        self.id = id
        self.sorted = False
        self.players = players
        self.team_1 = []
        self.team_2 = []
        self.votes = {}
    
    def add_vote(self, player, vote):
        already_voted = False

        if player in self.votes:
            self.votes.update({player:vote})
            if self.vote_records[i] == player:
                already_voted = True
                voter_index = i
        
        if already_voted:
            self.votes[voter_index] = vote
        else:
            self.votes.append(vote)
            self.vote_records.append(player)

        return already_voted

    def count_votes(self):
        vote_tally = {
            'r_count': 0,
            'c_count': 0,
            'b_count': 0,
            'o_count': 0
        }

        if len(self.votes) < 8:
            return
        
        for vote in self.votes
            if vote == 'random':
                vote_tally.update('r_count' : vote_tally.r_count+1)
            elif vote == 'captains':
                c_count += 1
            elif vote == 'balance':
                b_count += 1
            elif vote == 'ordered':
                o_count += 1
            else:
                print('Thats is a spicya vote!')

        vote_win = max()

        # tally votes for the 4 things
        # no majority?
        # else call
    
    def randomize(self):
        unsorded_players = self.players
        
        for i in (0, len(self.players)/2):
            self.team_1.append(unsorted_players.remove(unsorted_players[random.randint(0, len(self.players)-1)]))
            self.team_2.append(unsorted_players.remove(unsorted_players[random.randint(0, len(self.players)-1)]))

        self.sorted = True

    def captains(self):
        # Randomly select 2 captains from player list
        # learn how to dm captins
        # they react with who they want (or respond)
        self.sorted = True

    # Assign teams based on their combined mmr
    def balance(self):
        # TODO: Write algorithm to balance total mmr
        # NOTE: Cannot be completed until the server mmr is saved to a DB
        self.sorted = True

    # Assign teams based on the order they joined the queue
    def ordered(self):
        for i in range(0, (len(self.players)/2)):
            self.team_1.append(players[i])

        for i in range(len(self.players)/2, len(self.players)):
            self.team_2.append(players[i])

        self.sorted = True