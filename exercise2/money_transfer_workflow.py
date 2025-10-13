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
        
        # Step 1: Execute withdraw activity with 5 second timeout
        await workflow.execute_activity(
            withdraw,
            args=[request.from_account, request.amount],
            start_to_close_timeout=timedelta(seconds=5),
        )
        
        workflow.logger.info("Withdrawal completed")
        
        # Step 2: Wait for approval signal using workflow.wait_condition
        workflow.logger.info("Waiting for approval...")
        # TODO: Use workflow.wait_condition to wait for approval_received
        
        if self.approved:
            # Step 3a: If approved, execute deposit activity
            # TODO: Use workflow.execute_activity with deposit function
            
            workflow.logger.info("Transfer approved and completed")
            return "Transfer completed successfully"
        else:
            # Step 3b: If not approved, execute refund activity
            # TODO: Use workflow.execute_activity with refund function
            
            workflow.logger.info("Transfer rejected and refunded")
            return "Transfer rejected and refunded"

    @workflow.signal
    async def approve(self, approved: bool) -> None:
        # TODO: Implement approval signal handler
        # - Log the approval decision
        # - Update the workflow state
        pass
