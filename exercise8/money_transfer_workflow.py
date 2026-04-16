from datetime import timedelta
from enum import Enum
from temporalio import workflow
from temporalio.exceptions import ActivityError
from transfer_request import TransferRequest
from retry_update import RetryUpdate

with workflow.unsafe.imports_passed_through():
    from banking_activities import withdraw, deposit, refund
    # TODO: Task 1 - Import send_notification activity


class TransferStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"


@workflow.defn
class MoneyTransferWorkflow:
    def __init__(self) -> None:
        self.approved = False
        self.status = TransferStatus.PENDING
        self.retry_requested = False
        self.request = None

    @workflow.run
    async def transfer(self, request: TransferRequest) -> str:
        workflow.logger.info(f"Starting transfer: {request}")
        self.status = TransferStatus.IN_PROGRESS
        self.request = request

        try:
            # Step 1: Withdraw from source account
            await self._execute_with_manual_retry(
                lambda: workflow.execute_activity(
                    withdraw,
                    args=[self.request.from_account, self.request.amount],
                    start_to_close_timeout=timedelta(seconds=5),
                )
            )

            # Step 2: Wait for approval
            await workflow.wait_condition(lambda: self.approved)

            # Step 3: Deposit to target account
            await self._execute_with_manual_retry(
                lambda: workflow.execute_activity(
                    deposit,
                    args=[self.request.to_account, self.request.amount],
                    start_to_close_timeout=timedelta(seconds=5),
                )
            )

            # TODO: Task 2 - Add versioning with workflow.patched("add-notification")
            # Use workflow.patched() to conditionally call send_notification
            # if workflow.patched("add-notification"):
            #     await workflow.execute_activity(
            #         send_notification,
            #         args=[self.request.to_account, self.request.amount],
            #         start_to_close_timeout=timedelta(seconds=5),
            #     )

            self.status = TransferStatus.COMPLETED
            return "Transfer completed successfully"

        except ActivityError as e:
            await self._execute_with_manual_retry(
                lambda: workflow.execute_activity(
                    refund,
                    args=[self.request.from_account, self.request.amount],
                    start_to_close_timeout=timedelta(seconds=5),
                )
            )
            self.status = TransferStatus.FAILED
            return f"Transfer failed: {str(e)}"

    async def _execute_with_manual_retry(self, operation):
        while True:
            try:
                return await operation()
            except ActivityError:
                self.status = TransferStatus.RETRYING
                self.retry_requested = False
                await workflow.wait_condition(lambda: self.retry_requested)

    @workflow.signal
    async def approve(self, approved: bool) -> None:
        workflow.logger.info(f"Approval received: {approved}")
        self.approved = approved

    @workflow.signal
    async def retry(self, update: RetryUpdate) -> None:
        if update.key == "fromAccount":
            self.request.from_account = update.value
        elif update.key == "toAccount":
            self.request.to_account = update.value
        elif update.key == "amount":
            self.request.amount = float(update.value)
        self.retry_requested = True

    @workflow.query
    def get_status(self) -> str:
        return self.status.value

    @workflow.query
    def is_approved(self) -> bool:
        return self.approved
