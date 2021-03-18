import calendar
import time


def check_and_wait_limit(github_client):
    rate_limit = github_client.get_rate_limit().core
    reset_timestamp = calendar.timegm(rate_limit.reset.timetuple())

    print('Limit Remaining: {limit} || Next Reset At: {next_reset}'.format(limit=rate_limit.remaining, next_reset=time.ctime(reset_timestamp)))

    if rate_limit.remaining < 500:
        # add 10 seconds to be sure the rate limit has been reset
        sleep_time = reset_timestamp - calendar.timegm(time.gmtime()) + 10
        print('Less than 500 limit reached, going to sleep for {} seconds'.format(sleep_time))
        time.sleep(sleep_time)