import ldap

class Connection:
    def __init__(self, ip, user_at_host, password):
        self.AD_address = 'ldap://' + ip
        self.user_at_host = user_at_host
        self.password = password
        self.connection = None
        self.connect()

    def connect(self):
        try:
            connection = ldap.initialize(self.AD_address)
            connection.protocol_version = 3
            connection.set_option(ldap.OPT_REFERRALS, 0)
            connection.simple_bind_s(self.user_at_host, self.password)
            self.connection = connection

        except ldap.INVALID_CREDENTIALS:
            print("Your username or password is incorrect.")

        except ldap.SERVER_DOWN:
            print("The server appears to be down.")

        except ldap.LDAPError, e:
            if type(e.message) == dict and e.message.has_key('desc'):
                print e.message['desc']
            else: 
                print e

        print 'Connection to AD server successful!\n'


    def close(self):
        self.connection.unbind_s()


    def search(self, username):
        """ Searches Active Directory for specific username.
            Returns entities user is a member of as a list if user is found """

        # Check that connection exists already
        if self.connection == None:
            'Search failed - No connection to AD server exists.'
            exit()

        ldap_filter = 'sAMAccountName=' + username
        attr_filter = ['memberOf']
        basedn = "DC=maincampus,DC=isqchina,DC=com"
        results = self.connection.search_s(basedn, ldap.SCOPE_SUBTREE, ldap_filter, attr_filter)

        return self.__results_to_list(results)


    def __results_to_list(self, results):

        # Are there results at all?
        if len(results) is not 0:

            for key,val in results:

                # Ignore empty results
                if key != None:
                    memberOf = val['memberOf']                          # ['CN=example,OU=example,...']
                    memberOf = self.__extract_item_from_list(memberOf)  # 'CN=example,OU=example,...'
                    memberOf = self.__split_csv_string(memberOf)        # 'CN=example', 'CN=example'

        # Pull out values from memberOf
        entities = []
        for item in memberOf:
            key,val = item.split('=')
            entities.append(val)

        return entities
        

    def __extract_item_from_list(self, one_item_list):
        return one_item_list[0]

    def __split_csv_string(self, item_list):
        return item_list.split(',')

    def display(self):
        print {"address": self.AD_address, "username": self.user_at_host, "password": self.password}

