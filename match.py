import random
import math

class Match:
    def __init__(self, id, players, guild):
        self.id = id
        self.guild = guild
        self.players = players # List
        self.number_of_players = len(self.players)
        self.host = self.players[random.randint(0, self.number_of_players-1)]
        self.team_1 = []
        self.team_2 = []
        self.mode_maps = {}

        self.team_captains = []
        self.active_captain = 0
        self.messages = []
                
        self.mode_selected = False
        self.unsorted_players = self.players.copy()
        self.votes = {}
        self.selection_mode = ''
        self.vcs = []

        self.maps = ['Live Fire', 'Recharge', 'Streets', 'Aquarius', 'Bazaar']
        self.game_modes = {
            'Slayer': ['Live Fire', 'Recharge', 'Streets', 'Aquarius', 'Bazaar'],
            'Odd Ball': ['Live Fire', 'Recharge', 'Streets'],
            'Strongholds': ['Live Fire', 'Recharge', 'Streets'],
            'CTF': ['Aquarius', 'Bazaar']
        }
        self.generate_maps()
    
# Vote processing methods -------------------------------------------------
    def add_vote(self, player, vote_type):
        already_voted = False
        if player in self.votes:
            already_voted = True   

        self.votes.update({player:vote_type})
        return already_voted

    def recorded_voters(self):
        voter_list = []

        for player in self.players:
            if player in self.votes:
                voter_list.append(player)

        return voter_list

    def missing_voters(self):
        missing_list = []

        for player in self.players:
            if not player in self.votes:
                missing_list.append(player)

        return missing_list

    def count_votes(self, queue_max):        
        vote_tally = {
            'r_count': 0,
            'c_count': 0,
            'b_count': 0,
            'o_count': 0
        }

        # Tally votes
        for vote in self.votes:
            if self.votes[vote] == 'random':
                vote_tally.update({'r_count': vote_tally['r_count']+1})
            elif self.votes[vote] == 'captains':
                vote_tally.update({'c_count': vote_tally['c_count']+1})
            elif self.votes[vote] == 'balance':
                vote_tally.update({'b_count': vote_tally['b_count']+1})
            elif self.votes[vote] == 'ordered':
                vote_tally.update({'o_count': vote_tally['o_count']+1})

        # If 50% of the players vote for the same mode, it gets selected
        for vote_type in vote_tally:
            if vote_tally[vote_type] >= self.number_of_players/2:
                if vote_type == 'r_count':
                    self.randomize()
                elif vote_type == 'c_count':
                    self.captains()
                elif vote_type == 'b_count':
                    self.balance()
                elif vote_type == 'o_count':
                    self.ordered()
                
                return True

        # Make sure that everyone has a chance to vote
        if len(self.votes) < queue_max:
            return False

        # Find the largest value
        vote_win = max(vote_tally, key=vote_tally.get)
        max_value = vote_tally[vote_win]

        # Checks to see if there is a tie for the largest number of votes (See comment above for why)
        max_counter = 0
        tie_votes = []
        for vote in vote_tally:
            if vote_tally[vote] == max_value:
                max_counter += 1
                tie_votes.append(vote)

        # Randomizes the winning modes
        if max_counter > 1:
            vote_win = tie_votes[random.randint(0, len(tie_votes)-1)]

        # Call method for winning selection mode
        if vote_win == 'r_count':
            self.randomize()
        elif vote_win == 'c_count':
            self.captains()
        elif vote_win == 'b_count':
            self.balance()
        elif vote_win == 'o_count':
            self.ordered()
        
        return True
    
# Selection mode commands -------------------------------------------------
    # Randomly assigns teams
    def randomize(self):
        for i in range(math.ceil(self.number_of_players/2)):
            self.team_1.append(self.unsorted_players.pop(random.randint(0, len(self.unsorted_players)-1)))
            if len(self.unsorted_players) > 0:
                self.team_2.append(self.unsorted_players.pop(random.randint(0, len(self.unsorted_players)-1)))

        self.selection_mode = 'random'
        self.mode_selected = True

    # Assign 2 players the role of captain and then dm them to start picking teams
    def captains(self):
        # Randomly assign captains
        self.team_captains.append(self.unsorted_players.pop(random.randint(0, len(self.unsorted_players)-1)))
        self.team_1.append(self.team_captains[0])
        
        if len(self.unsorted_players) > 0:
            self.team_captains.append(self.unsorted_players.pop(random.randint(0, len(self.unsorted_players)-1)))
            self.team_2.append(self.team_captains[1])

        self.selection_mode = 'captains'
        self.mode_selected = True

    # Assign teams based on their combined mmr
    def balance(self):
        # TODO: Write algorithm to balance total mmr until this algorithm is written, use win/loss ratio instread
        # NOTE: Cannot be completed until the server mmr is saved to a DB
        self.selection_mode = 'balance'
        self.mode_selected = True

    # Assign teams based on the order they joined the queue
    def ordered(self):
        for i in range(math.ceil(self.number_of_players/2)):
            self.team_1.append(self.players[i])

        for i in range(math.ceil(self.number_of_players/2), self.number_of_players):
            self.team_2.append(self.players[i])

        self.selection_mode = 'ordered'
        self.mode_selected = True
    
# Game mode and map selection
    def generate_maps(self):
        self.game_modes.pop('Slayer')

        # Generates a list of 3 random maps
        selected_maps = []
        for i in range(3):
            selected_maps.append(self.maps.pop(random.randint(0, len(self.maps)-1)))

        # Select first game mode
        mode_selection = []
        for mode in self.game_modes:
            if selected_maps[0] in self.game_modes[mode]:
                mode_selection.append(mode)
        
        # Add first game mode an map to dictionary mode_maps
        selected_mode = mode_selection[random.randint(0, len(mode_selection)-1)]
        self.mode_maps.update({selected_mode: selected_maps[0]})
        self.game_modes.pop(selected_mode)

        # Add slayer and second map to dictionary mode_maps
        self.mode_maps.update({'Slayer': selected_maps[1]})

        # Selects the third game mode
        mode_selection = []
        # NOTE: This is a fix for an error that could occur here if
        # the third map selected wasn't present in the 2 remaining game modes
        while len(mode_selection) < 3:
            for mode in self.game_modes:
                if selected_maps[2] in self.game_modes[mode]:
                    mode_selection.append(mode)
            if len(mode_selection) < 3:
                selected_maps[2] = self.maps.pop(random.randint(0, len(self.maps)-1))
        
        # Add third game mode an map to dictionary mode_maps
        selected_mode = mode_selection[random.randint(0, len(mode_selection)-1)]
        self.mode_maps.update({selected_mode: selected_maps[2]})
        self.game_modes.pop(selected_mode)