import random

class Match:
    def __init__(self, id, players):
        self.id = id
        self.sorted = False
        self.players = players
        self.team_1 = []
        self.team_2 = []
        self.votes = {}
    
# Vote processing methods -------------------------------------------------
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

    def vote_check(self):
        voter_list = []

        for player in self.players
            if player in self.votes
                voter_list.append(player)

        return voter_list

    def count_votes(self, queue_max):
        # Checks for less than number of member votes
        if len(self.votes) < queue_max:
            return False
        
        vote_tally = {
            'r_count': 0,
            'c_count': 0,
            'b_count': 0,
            'o_count': 0
        }

        for vote in self.votes.values():
            if vote == 'random':
                vote_tally.update('r_count' : vote_tally.r_count+1)
            elif vote == 'captains':
                vote_tally.update('c_count' : vote_tally.r_count+1)
            elif vote == 'balance':
                vote_tally.update('b_count' : vote_tally.r_count+1)
            elif vote == 'ordered':
                vote_tally.update('o_count' : vote_tally.r_count+1)

        # Find the largest value (always returns the first highest instance of the max number)
        vote_win = max(vote_tally, key=vote_tally.get)
        max_value = vote_tally[vote_win]

        # Checks to see if there is a tie for the largest number of votes (See comment above for why)
        max_counter = 0
        for vote in vote_tally.values():
            if vote == max_value:
                max_counter += 1

        # Will result in "True" if a tie was found
        if max_counter > 1
            # There was a tie found, must prompt the user for additional attention
            # NOTE: Ask what should happen here if no majority
            return False

        # Call method for winning selection mode
        if vote_win == 'r_count':
            randomize()
        elif vote_win == 'c_count':
            captains()
        elif vote_win == 'b_count':
            balance()
        elif vote_win == 'o_count':
            ordered()
        
        return True
    
# Selection mode commands -------------------------------------------------
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