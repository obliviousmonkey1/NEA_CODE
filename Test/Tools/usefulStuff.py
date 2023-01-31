"""
File full of random pieces of code that i can use later 
"""


""" Search suggestion system """

class SP:
    def suggestedProducts(self, products: list[str], searchWord: str) -> list[list[str]]:
        """ 
        Sorts the list of products into alpahbetical order then has a pointer at the top 
        and pointer bottom. The pointer at the top works its way down till it finds a matching letter
        pointer at the bottom works its way up till it finds a maching letter. We know that since the 
        list has been sorted the values inbetween those two pointers will have the same letter in the same place
        .This program display the top 3.
        """
        res = []
        products.sort()

        l,r = 0, len(products) - 1
        for i in range(len(searchWord)):
            c = searchWord[i]

            while l <= r and (len(products[l]) <= i or products[l][i] != c):
                l += 1
            while 1 <= r and (len(products[r]) <= i or products[r][i] != c):
                r -= 1
            
            res.append([])
            remain = r - l + 1
            for j in range(min(3, remain)):
                res[-1].append(products[l + j])
        return res 
