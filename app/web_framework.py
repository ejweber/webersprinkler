import bottle, api_functions
import logging as log
from json import dumps # needed to return a top level JSON array

api_functions.set_up_logs()
api = api_functions.API()


@bottle.get('/programs')
@bottle.get('/programs/<program_id>')
def get_programs(program_id=None):
    if program_id is None:
        # must set content type manually and use dumps for top level array
        bottle.response.content_type = 'application/json'
        return dumps(api.programs)
    else:
        try:
            return api.get_program_by_id(program_id)
        except KeyError:
            log.warning('Attempted to retrieve unknown program: ' + program_id)
            bottle.abort(404, 'The specified program does not exist.')


@bottle.post('/programs')
@bottle.post('/programs/<program_id>')
def add_or_update(program_id=None):
    request = bottle.request
    log.debug('Content-Type: ' + request.get_header('Content-Type'))
    log.debug('Data: ' + str(request.json))
    if request.headers.get('Content-Type') != 'application/json':
        log.warning('Attempted POST without application/json header')
        bottle.abort(400, 'The application/json header is required.')
    if not api.get_program_by_id(program_id) and program_id is not None:
        log.warning('Attempted to update unknown program: ' + program_id)
        bottle.abort(404, 'The specified program does not exist.')
    try:
        if api.add_or_update(request.json, program_id) is True:
            if program_id is not None:
                return api.get_program_by_id(program_id)
            else:
                return api.programs
        else:
            log.warning('Attempted to create invalid program state')
            bottle.abort(400, 'Invalid parameters were supplied.')
    except ValueError:
        log.warning('JSON formatting error in body of request')
        bottle.abort(400, 'JSON formatting is incorrect.')
        
        
@bottle.delete('/programs/<program_id>')
@bottle.delete('/programs/<program_id>/<run_day>')
@bottle.delete('/programs/<program_id>/<run_day>/<run_hour>')
@bottle.delete('/programs/<program_id>/<run_day>/<run_hour>/<run_minute>')
def delete(program_id=None, run_day=None, run_hour=None, run_minute=None):
    run_time = None
    if run_day:
        try:
            run_time = run_day + ' ' + run_hour + ':' + run_minute
        except TypeError:
            log.warning('Attempted to delete a run time using incomplete ' +
                        'parameters')
            bottle.abort(404, 'Incomplete run time parameters supplied.')
    try:
        api.delete(program_id, run_time)
        if not run_time:
            return api.programs
        else:
            return api.programs[program_id]
    except KeyError:
        if not run_time:
            log.warning('Attempted to delete unknown program: ' + program_id)
            bottle.abort(404, 'The specified program does not exist.')
    except ValueError:
        log.warning('Attempted to delete unknown run time from program ' + 
                    program_id + ': ' + run_time)
        bottle.abort(404, 'The specified run time does not exist.')
            
            
@bottle.post('/run/program/<program_id>')
def run_program(program_id=None):
    try:
        api.run_program(program = api.get_program_by_id(program_id))
        return api.status
    except KeyError:
        log.warning('Attempted to run unknown program: ' + program_id)
        bottle.abort(404, 'The specified program does not exist.')


@bottle.post('/run/manual/<zone>')
@bottle.post('/run/manual/<zone>/<time>')
def run_manual(zone, time=-1):
    if not zone.isdigit():
        log.warning('Zone index not numeric: ' + zone)
        bottle.abort(404, 'Zones designators are positive integers.')
    try:
        api.run_manual(int(zone) - 1, time)
        return api.status
    except IndexError:
        log.warning('Attempted to run unknown zone index: ' + zone)
        bottle.abort(404, 'The specified zone does not exist.')


@bottle.get('/status')
@bottle.get('/status/<designator>')
def get_status(designator=None):
    if designator is None:
        return api.status
    try:
        return {designator: api.status[designator]}
    except KeyError:
        log.warning('Attempted to retrieve invalid status: ' + designator)
        bottle.abort(404, 'The specified status designator does not exist.')


@bottle.post('/stop')
def stop():
    api.stop_sprinklers(reschedule=True)
    return api.status


# typically only called internally
@bottle.post('/reschedule')
def reschedule():
    api.schedule_next_program()
    return api.status


# typically only called internally
@bottle.post('/recalculate')
def recalculate():
    api.choose_next_program()
    return api.status
