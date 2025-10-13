from datetime import timedelta
from temporalio import workflow
from transfer_request import TransferRequest

with workflow.unsafe.imports_passed_through():
    from banking_activities import withdraw, deposit, refund


@workflow.defn
class MoneyTransferWorkflow:
    def __init__(self) -> None:
        self.approved = False
        self.approval_received = False

    @workflow.run
    async def transfer(self, request: TransferRequest) -> str:
        workflow.logger.info(f"Starting transfer: {request}")
        
        # Step 1: Withdraw from source account
        await workflow.execute_activity(
            withdraw,
            args=[request.from_account, request.amount],
            start_to_close_timeout=timedelta(seconds=5),
        )
        workflow.logger.info("Withdrawal completed")
        
        # Step 2: Wait for approval
        workflow.logger.info("Waiting for approval...")
        await workflow.wait_condition(lambda: self.approval_received)
        
        if self.approved:
            # Step 3a: Approved - deposit to target account
            await workflow.execute_activity(
                deposit,
                args=[request.to_account, request.amount],
                start_to_close_timeout=timedelta(seconds=5),
            )
            workflow.logger.info("Transfer approved and completed")
            return "Transfer completed successfully"
        else:
            # Step 3b: Not approved - refund to source account
            await workflow.execute_activity(
                refund,
                args=[request.from_account, request.amount],
                start_to_close_timeout=timedelta(seconds=5),
            )
            workflow.logger.info("Transfer rejected and refunded")
            return "Transfer rejected and refunded"

    @workflow.signal
    async def approve(self, approved: bool) -> None:
        workflow.logger.info(f"Approval received: {approved}")
        self.approved = approved
        self.approval_received = True
