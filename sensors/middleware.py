import time 
def request_timer(get_response):
  def middleware(request):
    start_time= time.perf_counter()
    response = get_response(request)
    time_taken= time.perf_counter() - start_time
    print(f"The request '{request.path}' took {time_taken:.3f} seconds")
    return response
  return middleware