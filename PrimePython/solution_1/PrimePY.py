
# Python Prime Sieve
#
# MyFirstPython Program (tm) Dave Plummer 8/9/2018
#
# This is the main prime_sieve class. Call it with the number you wish as an
# upper limit, then call the runSieve method to do the calculation.
# printResults will dump the count to check validity.
#
# Updated 3/22/2021 for Dave's Garage episode comparing C++, C#, and Python

from sys import stdout     # So I can print without an automatic python newline
from math import sqrt      # Used by the sieve
import timeit              # For timing the durations


class prime_sieve(object):

    # Storage for sieve - since we filter evens, just half as many bits
    rawbits = None

    # Upper limit, highest prime we'll consider
    sieveSize = 0

    # Historical data for validating our results - the number of primes
    # to be found under some limit, such as 168 primes under 1000
    primeCounts = {
        10: 4,
        100: 25,
        1000: 168,
        10000: 1229,
        100000: 9592,
        1000000: 78498,
        10000000: 664579,
        100000000: 5761455
    }

    def __init__(self, limit):
        self.sieveSize = limit
        self.rawbits = [True] * (int((self.sieveSize+1)/2))

    # Look up our count of primes in the historical data (if we have it) to see
    # if it matches
    # Check to see if this is an upper_limit we can
    # the data, and (b) our count matches. Since it will return
    # false for an unknown upper_limit, can't assume false == bad
    def validateResults(self):
        if self.sieveSize in self.primeCounts:
            return self.primeCounts[self.sieveSize] == self.countPrimes()
        return False

    # GetBit
    #
    # Gets a bit from the array of bits, but automatically just filters out
    # even numbers as false, and then only uses half as many bits for
    # actual storage

    def GetBit(self, index):

        if index % 2 == 0:
            # even numbers are automaticallty returned as non-prime
            return False
        else:
            return self.rawbits[int(index/2)]

    # ClearBit
    #
    # Reciprocal of GetBit, ignores even numbers and just stores the odds.
    # Since the prime sieve work should never waste time clearing even numbers,
    # this code will assert if you try to

    def ClearBit(self, index):

        if index % 2 == 0:
            assert("If you're setting even bits, "
                   "you're sub-optimal for some reason!")
            return False
        else:
            self.rawbits[int(index/2)] = False

    # primeSieve
    #
    # Calculate the primes up to the specified limit

    def runSieve(self):

        factor = 3
        q = sqrt(self.sieveSize)

        while factor < q:
            for num in range(factor, self.sieveSize):
                if self.GetBit(num) is True:
                    factor = num
                    break

            # If marking factor 3, you wouldn't mark 6 (it's a mult of 2)
            # so start with the 3rd instance of this factor's multiple.
            # We can then step by factor * 2 because every second one
            # is going to be even by definition

            for num in range(factor * 3, self.sieveSize, factor * 2):
                self.ClearBit(num)

            # No need to check evens, so skip to next odd
            # (factor = 3, 5, 7, 9...)
            factor += 2

    # countPrimes
    #
    # Return the count of bits that are still set in the sieve. Assumes you've
    # already called runSieve, of course!

    def countPrimes(self):
        return sum(1 for b in self.rawbits if b)

    # printResults
    #
    # Displays the primes found
    # (or just the total count, depending on what you ask for)

    def printResults(self, showResults, duration, passes):

        # Since we auto-filter evens, we have to special case the number 2
        # which is prime
        if showResults:
            stdout.write("2, ")

        count = 1
        # Count (and optionally dump) the primes
        # that were found below the limit
        for num in range(3, self.sieveSize):
            if self.GetBit(num) is True:
                if (showResults):
                    stdout.write(str(num) + ", ")
                count += 1

        assert(count == self.countPrimes())
        stdout.write("\n")
        print(f"Passes: {passes}, Time: {duration}, Avg: {duration/passes}, "
              f"Limit: {self.sieveSize}, Count: {count}, "
              f"Valid: {self.validateResults()}")

        # Following 2 lines added by rbergen to conform to
        # drag race output format
        stdout.write("\n")
        print(f"davepl;{passes};{duration};1;algorithm=base,faithful=yes")


# MAIN Entry
if __name__ == "__main__":
    # Record our starting time
    tStart = timeit.default_timer()

    # We're going to count how many passes we make in fixed window of time
    passes = 0

    # Run until more than 10 seconds have elapsed
    while timeit.default_timer() - tStart < 5:
        #  Calc the primes up to a million
        sieve = prime_sieve(1000000)
        #  Find the results
        sieve.runSieve()
        #  Count this pass
        passes = passes + 1

    # After the "at least 10 seconds", get the actual elapsed
    tD = timeit.default_timer() - tStart

    sieve.printResults(False, tD, passes)                   # Display outcome
