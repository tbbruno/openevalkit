import docker
from io import BytesIO
import tarfile
import os

from openevalkit.core.code_runner import CodeRunner

class DockerPythonCodeRunner(CodeRunner):
    """
    A class that runs Python code inside a Docker container.
    This code runner provides a sandboxed environment for executing unverified code safely.

    Note: Docker must be installed and running with proper permissions on the user's machine.
    """

    def exec(self, code) -> None:
        """
        Execute the given Python code inside a Docker container.

        Args:
            code (str): The Python code to execute.

        Returns:
            str: The output of the executed code.

        Raises:
            Exception: If the exit code of the container is non-zero.
        """
        # Write the Python code to a file
        script_path = 'temp_script.py'
        with open(script_path, 'w') as file:
            file.write(code)

        # Dockerfile as a string
        dockerfile = f'''
        FROM python:3.9-slim
        RUN apt-get update && apt-get install -y python3
        COPY {script_path} /app/{script_path}
        WORKDIR /app
        CMD ["python", "{script_path}"]
        '''

        # Create a Docker client
        client = docker.from_env()

        # Create a file-like object for the Dockerfile
        dockerfile_fileobj = BytesIO(dockerfile.encode('utf-8'))

        # Create a tarfile with the Dockerfile and the temporary Python script
        tarstream = BytesIO()
        tar = tarfile.TarFile(fileobj=tarstream, mode='w')
        tarinfo = tarfile.TarInfo(name='Dockerfile')
        tarinfo.size = len(dockerfile_fileobj.getvalue())
        tar.addfile(tarinfo, dockerfile_fileobj)
        tar.add(script_path, arcname=script_path)
        tar.close()

        tarstream.seek(0)

        # Build the Docker image
        container_tag = 'python-sandbox'
        _, _ = client.images.build(fileobj=tarstream, custom_context=True, tag=container_tag, rm=True)

        # Create and run the container
        container = client.containers.run(container_tag, detach=True)

        # Wait for the container to finish running
        container.wait()

        # Wait for the container to finish running
        exit_code = container.wait()['StatusCode']

        # Get the output
        output = container.logs()

        # Clean up: Remove the container and the image
        container.remove()
        client.images.remove(image=container_tag, force=True)

        # Remove the temporary script file
        os.remove(script_path)

        # If the exit code is non-zero, raise an exception with the output
        if exit_code != 0:
            raise Exception(output.decode('utf-8'))

        # Return the output
        return output.decode('utf-8')
