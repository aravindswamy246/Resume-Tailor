import asyncio
import click
from pathlib import Path
from resume_tailor import ResumeTailor
from services import ResumeService  # Use the same service
import os


@click.command()
@click.argument('resume', type=click.Path(exists=True))
@click.argument('job', type=click.Path(exists=True))
@click.option('--tone', '-t',
              type=click.Choice(['professional', 'casual', 'academic']),
              default='professional')
async def main(resume, job, tone):
    """Resume tailoring tool."""
    # Use the same service layer as API
    service = ResumeService()

    try:
        result = await service.tailor_resume(
            resume_text=Path(resume).read_text(),
            job_description=Path(job).read_text(),
            tone=tone
        )
        click.echo(result)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == "__main__":
    asyncio.run(main())
